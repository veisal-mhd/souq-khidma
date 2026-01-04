from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from transactions.models import Transaction
from .services import get_payment_service


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initier_paiement(request):
    """
    Initie un paiement pour une transaction
    """
    transaction_id = request.data.get('transaction_id')
    mode_paiement = request.data.get('mode_paiement')
    
    if not transaction_id or not mode_paiement:
        return Response(
            {'error': 'transaction_id et mode_paiement sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        transaction = Transaction.objects.get(id=transaction_id, client=request.user)
    except Transaction.DoesNotExist:
        return Response(
            {'error': 'Transaction introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if transaction.statut != 'en_attente':
        return Response(
            {'error': 'Cette transaction ne peut plus être payée'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtenir le service de paiement approprié
    try:
        payment_service = get_payment_service(mode_paiement)
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Traiter le paiement
    user_info = {
        'telephone': request.user.telephone,
        'email': request.user.email,
        'nom': f"{request.user.first_name} {request.user.last_name}"
    }
    
    result = payment_service.process_payment(
        amount=transaction.montant_total,
        reference=f"TXN_{transaction.id}",
        user_info=user_info
    )
    
    if result.get('success'):
        transaction.mode_paiement = mode_paiement
        transaction.transaction_id_externe = result.get('transaction_id', '')
        transaction.statut = 'paye'
        transaction.save()
        
        return Response({
            'success': True,
            'transaction_id': transaction.id,
            'payment_data': result,
            'message': 'Paiement initié avec succès'
        })
    else:
        return Response(
            {'error': result.get('error', 'Erreur lors du paiement')},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verifier_paiement(request):
    """
    Vérifie le statut d'un paiement
    """
    transaction_id = request.data.get('transaction_id')
    
    if not transaction_id:
        return Response(
            {'error': 'transaction_id est requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return Response(
            {'error': 'Transaction introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not transaction.transaction_id_externe:
        return Response(
            {'error': 'Aucune transaction externe associée'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtenir le service de paiement approprié
    payment_service = get_payment_service(transaction.mode_paiement)
    
    # Vérifier le paiement
    result = payment_service.verify_payment(transaction.transaction_id_externe)
    
    if result.get('status') == 'completed' and transaction.statut == 'paye':
        transaction.statut = 'en_escrow'
        transaction.save()
    
    return Response({
        'transaction_id': transaction.id,
        'status': transaction.statut,
        'verification': result
    })

