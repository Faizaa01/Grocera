from order.services import OrderService
from order import serializers as orderSz
from api.permissions import IsSellerOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from order.models import Wishlist, Cart, CartItem, Order
from order.endpoints import OrderEndpoints, CartEndpoints, WishlistEndpoints
from order.serializers import WishlistSerializer, CartSerializer, CartItemSerializer,AddCartItemSerializer, UpdateCartItemSerializer, EmptySerializer



class WishlistViewSet(ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Wishlist.objects.none()
        return Wishlist.objects.filter(user=self.request.user).order_by('-added_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @WishlistEndpoints.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @WishlistEndpoints.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @WishlistEndpoints.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @WishlistEndpoints.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @WishlistEndpoints.remove
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class CartViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)
    
    
    @CartEndpoints.list
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk'))
    

    @CartEndpoints.list_items
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CartEndpoints.retrieve_item
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @CartEndpoints.add
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CartEndpoints.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @CartEndpoints.remove
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




class OrderViewset(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        if self.request.user.groups.filter(name="Seller").exists():
            return Order.objects.prefetch_related('items__product').filter(items__product__seller=self.request.user).distinct()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    @OrderEndpoints.cancel
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status': 'Order canceled'})

    @OrderEndpoints.update_status
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = orderSz.UpdateOrderSerializer(
            order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Order status updated to {request.data['status']}'})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsSellerOrAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return orderSz.EmptySerializer
        if self.action == 'create':
            return orderSz.CreateOrderSerializer
        elif self.action == 'update_status':
            return orderSz.UpdateOrderSerializer
        return orderSz.OrderSerializer
    
 

    @OrderEndpoints.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @OrderEndpoints.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @OrderEndpoints.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @OrderEndpoints.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



