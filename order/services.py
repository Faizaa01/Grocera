from users.models import User
from django.db import transaction
from order.models import Cart, OrderItem, Order
from rest_framework.exceptions import PermissionDenied, ValidationError


class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('product').all()
            user = User.objects.get(pk=user_id)
            total_price = sum([item.product.price * item.quantity for item in cart_items])
            
            if user.balance < total_price:
                raise ValidationError("Insufficient balance. Please deposit more funds.")
            if not user.address:
                raise ValidationError("Address is required for order confirmation.")
            
            user.balance -= total_price
            user.save()

            order = Order.objects.create(user_id=user_id, total_price=total_price)
            order_items = []
            for item in cart_items:
                if item.product.stock < item.quantity:
                    raise ValidationError(f"Not enough stock for product {item.product.name}")
                
                order_items.append(OrderItem(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity
                ))
                item.product.stock -= item.quantity
                item.product.save()

            OrderItem.objects.bulk_create(order_items)
            cart.delete()
            return order

    @staticmethod
    def cancel_order(order, user):
        if user.is_staff:
            order.status = Order.CANCELED
            order.save()
            return order

        if order.user != user:
            raise PermissionDenied(
                {"detail": "You can only cancel your own order"})

        if order.status == Order.DELIVERED:
            raise ValidationError({"detail": "You can not cancel an order"})

        order.status = Order.CANCELED
        order.save()
        return order
