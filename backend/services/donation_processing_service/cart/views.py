from django.contrib.admindocs.views import user_has_model_view_permission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .utils import (validate_user_id_with_service, validate_cause_with_service,
                    validate_request, get_user_email_from_service, get_recipient_id_from_service)
from .decorators import extract_user_from_token
from donations.models import Donation
from payments.models import PaymentTransaction
from payments.paystack import Paystack

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
@extract_user_from_token
@validate_request
def get_cart(request):
    # User ID is now available in request.user_id
    validate_user_id_with_service(request.user_id, request)
    cart, _ = Cart.objects.get_or_create(user_id=request.user_id)
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@extract_user_from_token
@validate_request
def add_to_cart(request):
    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        validate_user_id_with_service(request.user_id, request)
        validate_cause_with_service(serializer.validated_data['cause_id'], request)

        cart, created = Cart.objects.get_or_create(
            user_id=request.user_id,
            status='active',
            defaults={'user_id': request.user_id}
        )

        existing_item = CartItem.objects.filter(
            cart=cart,
            cause_id=serializer.validated_data['cause_id']
        ).first()

        if existing_item:
            existing_item.quantity += serializer.validated_data.get('quantity', 1)
            existing_item.donation_amount = serializer.validated_data['donation_amount']
            existing_item.save()
            return Response(CartItemSerializer(existing_item).data, status=status.HTTP_200_OK)
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                cause_id=serializer.validated_data['cause_id'],
                quantity=serializer.validated_data.get('quantity', 1),
                donation_amount=serializer.validated_data['donation_amount']
            )
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly])
@extract_user_from_token
@validate_request
def update_cart_item(request, item_id):
    validate_user_id_with_service(request.user_id, request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user_id=request.user_id)
    quantity = request.data.get('quantity', cart_item.quantity)

    if quantity <= 0:
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

    cart_item.quantity = quantity
    cart_item.save()
    return Response({"message": "Cart item updated"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
@extract_user_from_token
@validate_request
def remove_from_cart(request, item_id):
    validate_user_id_with_service(request.user_id, request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user_id=request.user_id)
    cart_item.delete()
    return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@extract_user_from_token
@validate_request
def checkout(request):
    cart = get_object_or_404(Cart, user_id=request.user_id)
    if not cart.items.exists():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = sum(item.donation_amount * item.quantity for item in cart.items.all())

    donations = []
    for item in cart.items.all():
        # Get recipient ID from cause service
        try:
            recipient_id = get_recipient_id_from_service(item.cause_id, request)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        donation = Donation.objects.create(
            user_id=request.user_id,
            cause_id=item.cause_id,
            amount=item.donation_amount * item.quantity,
            currency='GHS',
            status='pending',
            recipient_id=recipient_id
        )
        donations.append(donation)

    # Get user email from user_service
    try:
        user_email = get_user_email_from_service(request.user_id, request)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Initialize payment with Paystack
    paystack_response = Paystack.initialize_payment(user_email, total_amount)

    if paystack_response['status']:
        data = paystack_response['data']
        payment_transaction = PaymentTransaction.objects.create(
            donation=donations[0],
            user_id=request.user_id,
            amount=total_amount,
            currency='GHS',
            transaction_id=data['reference'],
            status='pending',
            payment_method='Paystack',
        )
        cart.status = 'completed'
        cart.save()
        return Response({
            'authorization_url': data['authorization_url'],
            'reference': data['reference'],
            'total_amount': total_amount,
            'payment_id': payment_transaction.id
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": paystack_response['message']}, status=status.HTTP_400_BAD_REQUEST)