from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from .utils import validate_user_id_with_service, validate_cause_with_service, validate_event_with_service
from ..donations.models import Donation


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user.id)
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_to_cart(request):
    user_id = request.user.id
    validated_user_id = validate_user_id_with_service(user_id)

    # Either event or cause ID should be provided
    event_or_cause_id = request.data.get('event_or_cause_id')
    item_type = request.data.get('type') # event or cause
    donation_amount = request.data.get('donation_amount')
    quantity = request.data.get('quantity')

    if not event_or_cause_id or not item_type or not donation_amount:
        return Response ({
            "error": "event_or_cause_id, type and donation_amount are required."
        }, status=status.HTTP_400_BAD_REQUEST)

        # Validate based on the type of item being added
    if item_type == 'event':
        validated_id = validate_event_with_service(event_or_cause_id)
    elif item_type == 'cause':
        validated_id = validate_cause_with_service(event_or_cause_id)
    else:
        return Response({
            "error": "Invalid type. Must be 'event' or 'cause'."
        }, status=status.HTTP_400_BAD_REQUEST)

    cart, _ = Cart.objects.get_or_create(user_id=validated_user_id)
    cart_item, _ = CartItem.objects.get_or_create(cart=cart, item_type=item_type, donation_amount=donation_amount)
    cart_item.quantity = quantity if quantity is not None else cart_item.quantity
    cart_item.save()
    return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
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
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user.id)
    cart_item.delete()
    return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

@api_view['POST']
@permission_classes([IsAuthenticatedOrReadOnly])
def checkout(request):
    user_id = request.user.id
    cart = get_object_or_404(Cart, user_id=user_id)
    if not cart.items.all():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = sum(item.donation_amount * item.quantity for item in cart.items.all())

    try:
        for cart_item in cart.items.all():
            Donation.objects.create(
                user=user_id,
                event_or_cause_id=cart_item.event_or_cause_id,
                amount=cart_item.donation_amount * cart_item.quantity,
                status=cart_item.status,
            )

        payment_data = {
            "user_id": user_id,
            "amount": total_amount,
            "payment_method": request.data.get("payment_method"),
            "status": "completed"
        }
