from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .utils import validate_user_id_with_service, validate_cause_with_service, validate_event_with_service
from donations.models import Donation
from payments.models import PaymentTransaction
from payments.paystack import Paystack


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_cart(request):
    cart, _ = Cart.objects.get_or_create(user_id=request.user.id)
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_to_cart(request):
    user_id = request.user.id
    validated_user_id = validate_user_id_with_service(user_id)

    # Either event or cause ID should be provided
    cause_id = request.data.get('cause_id')
    donation_amount = request.data.get('donation_amount')
    quantity = request.data.get('quantity')

    if not cause_id or not donation_amount:
        return Response ({
            "error": "cause_id, type and donation_amount are required."
        }, status=status.HTTP_400_BAD_REQUEST)


    validated_cause_id = validate_cause_with_service(cause_id)

    cart, _ = Cart.objects.get_or_create(user_id=validated_user_id)
    cart_item, created  = CartItem.objects.get_or_create(
        cart=cart,
        cause_id=validated_cause_id,
        defaults={'donation_amount': donation_amount, 'quantity': quantity}
    )
    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user_id=request.user.id)
    quantity = request.data.get('quantity', cart_item.quantity)
    if quantity <= 0:
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
    cart_item.quantity = quantity
    cart_item.save()
    return Response({"message": "Cart item updated"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user_id=request.user.id)
    cart_item.delete()
    return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def checkout(request):
    user_id = request.user.id
    cart = get_object_or_404(Cart, user_id=user_id)
    if not cart.items.exists():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = sum(item.donation_amount * item.quantity for item in cart.items.all())

    donations = []
    for item in cart.items.all():
        donation = Donation.objects.create(
            user_id=request.user.id,
            cause_id=item.cause_id,
            amount=item.donation_amount * item.quantity,
            currency='GHS',
            status='pending',
            recipient_id=None
        )
        donations.append(donation)

    # Initiate payment
    paystack_response = Paystack.initialize_payment()
    if paystack_response['status']:
        data = paystack_response['data']
        PaymentTransaction.objects.create(
            donation=donations[0],  # Assuming the first donation is the main one
            user_id=user_id,
            amount=total_amount,
            currency='GHS',
            transaction_id=data['transaction_id'],
            status='pending',
            payment_method='Paystack',
        )
        cart.status = 'completed'
        cart.save()
        return Response ({'authorization_url': data['authorization_url']}, status=status.HTTP_200_OK)
    return Response({"error": paystack_response['message']}, status=status.HTTP_400_BAD_REQUEST)