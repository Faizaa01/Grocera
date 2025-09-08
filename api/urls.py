from django.urls import path,include
from rest_framework_nested import routers
from product.views import ProductViewSet, ProductImageViewSet, CategoryViewSet, ReviewViewSet
from order.views import WishlistViewSet, CartViewSet, CartItemViewSet, OrderViewset, HasOrderedProduct
from users.views import DepositViewSet, DashboardView, initiate_payment, payment_success, payment_cancel, payment_fail


router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('Wishlist', WishlistViewSet, basename='wishlist')
router.register('cart', CartViewSet, basename='cart')
router.register('orders', OrderViewset, basename='orders')
router.register('deposits', DepositViewSet, basename='deposit')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewSet, basename='product-images')

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
category_router.register('products', ProductViewSet, basename='category-products')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(category_router.urls)),
    path('', include(cart_router.urls)),
    path('cart/', CartViewSet.as_view({'get': 'retrieve'}), name='my-cart'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('orders/has-ordered/<int:product_id>/', HasOrderedProduct.as_view()),
    path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path("payment/success/", payment_success, name="payment-success"),
    path("payment/fail/", payment_fail, name="payment-fail"),
    path("payment/cancel/", payment_cancel, name="payment-cancel"),
]