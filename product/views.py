from drf_yasg import openapi
from django.db.models import Count
from product.filters import ProductFilter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from product.paginations import DefaultPagination
from rest_framework.exceptions import PermissionDenied
from product.permissions import IsReviewWriterOrReadonly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from product.models import Product, ProductImage, Category, Review
from api.permissions import IsAdminOrReadOnly, IsSellerOrAdmin, IsSeller
from product.endpoints import CategoryEndpoints, ProductEndpoints, ReviewEndpoints, ProductImageEndpoints
from product.serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at','name']

    def get_permissions(self):
        if self.action in ['create']:
            return [IsSeller()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsSellerOrAdmin()]
        return [AllowAny()]
    

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.kwargs.get('category_pk')

        if self.request.user.groups.filter(name='seller').exists():
            queryset = queryset.filter(seller=self.request.user)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @ProductEndpoints.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @ProductEndpoints.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @ProductEndpoints.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @ProductEndpoints.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @ProductEndpoints.remove
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    
class ProductImageViewSet(ModelViewSet):
    permission_classes = [IsSellerOrAdmin]
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        product = Product.objects.get(pk=self.kwargs.get('product_pk'))
        if not (product.seller==self.request.user):
            raise PermissionDenied("You can't add images to this product.")
        serializer.save(product=product)

    
    @ProductImageEndpoints.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @ProductImageEndpoints.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @ProductImageEndpoints.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @ProductImageEndpoints.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @ProductImageEndpoints.remove
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    queryset = Category.objects.annotate(product_count=Count('products')).all()

    @CategoryEndpoints.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CategoryEndpoints.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CategoryEndpoints.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CategoryEndpoints.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @CategoryEndpoints.remove
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewWriterOrReadonly]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)
    

    @ReviewEndpoints.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @ReviewEndpoints.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @ReviewEndpoints.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @ReviewEndpoints.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @ReviewEndpoints.partial_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @ReviewEndpoints.remove
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

