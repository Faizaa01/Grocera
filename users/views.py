from .models import Deposit
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from order.models import OrderItem
from product.models import Product
from rest_framework.views import APIView
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, DepositSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    
    @swagger_auto_schema(
        operation_summary="Retrieve dashboard data tailored for Admin/Seller.",
        operation_description="Returns dashboard info specific to the user's role (admin or seller).",
        responses={200: openapi.Response('Dashboard data')}
    )
    def get(self, request):
        user = request.user
        seller_group = Group.objects.get(name='Seller')

        if user.is_staff:
            total_products = Product.objects.count()
            total_orders = OrderItem.objects.count()
            products = Product.objects.all().values('id', 'name', 'seller__email', 'stock')

            return Response({
                'role': 'admin',
                'total_products': total_products,
                'total_orders': total_orders,
                'products': list(products),
            })

        elif seller_group in user.groups.all():
            seller_products = Product.objects.filter(seller=user)
            product_ids = seller_products.values_list('id', flat=True)
            sales = OrderItem.objects.filter(product_id__in=product_ids)

            total_products = seller_products.count()
            total_sales = sales.count()
            total_revenue = sum([item.total_price for item in sales])

            return Response({
                'role': 'seller',
                'total_products': total_products,
                'total_sales': total_sales,
                'total_revenue': total_revenue,
                'products': list(seller_products.values('id', 'name', 'stock')),
            })

        else:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        


class DepositViewSet(ModelViewSet):

    serializer_class = DepositSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Deposit.objects.none()
        if self.request.user.is_staff:
            return Deposit.objects.all()
        return Deposit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List Deposits",
        operation_description="Lists deposits for the logged-in user. Staff can see all deposits.",
        responses={200: DepositSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Deposit",
        operation_description="Retrieve details of a specific deposit by ID.",
        responses={200: DepositSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Deposit",
        operation_description="Create a new deposit for the logged-in user.",
        request_body=DepositSerializer,
        responses={201: DepositSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Deposit",
        operation_description="Update details of an existing deposit.",
        request_body=DepositSerializer,
        responses={200: DepositSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Deposit",
        operation_description="Delete a deposit record.",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
