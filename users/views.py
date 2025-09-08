from .models import Deposit
from drf_yasg import openapi
from rest_framework import status
from product.models import Product
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.views import APIView
from order.models import OrderItem, Order
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from django.shortcuts import HttpResponseRedirect
from django.conf import settings as main_settings
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, DepositSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

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
        seller_group = Group.objects.get(name='seller')

        total_users = User.objects.count()
        total_sellers = User.objects.filter(groups__name='seller').count()

        if user.is_staff:
            total_products = Product.objects.count()
            total_orders = OrderItem.objects.count()
            products = Product.objects.all().values('id', 'name', 'seller__email', 'stock')

            return Response({
                'role': 'admin',
                'total_products': total_products,
                'total_orders': total_orders,
                'total_users': total_users,
                'total_sellers': total_sellers,
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
                'total_users': total_users,
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




@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")

    deposit = Deposit.objects.create(
        user=user,
        amount=amount
    )

    settings = {'store_id': 'phima68a4a86fe8703',
                'store_pass': 'phima68a4a86fe8703@ssl', 'issandbox': True}
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"dep_{deposit.id}"
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number or "N/A"
    post_body['cus_add1'] = user.address or "N/A"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['product_name'] = "Wallet Deposit"
    post_body['product_category'] = "Deposit"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)
    # print("SSLCommerz Response:", response)

    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def payment_success(request):
    try:
        tran_id = request.data.get("tran_id") or request.GET.get("tran_id")
        deposit_id = tran_id.split('_')[1]
        deposit = Deposit.objects.get(id=deposit_id)
        deposit.status = "completed"
        deposit.user.balance += deposit.amount
        deposit.user.save()
        deposit.save()

        return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/payment/success/")
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
def payment_cancel(request):
    deposit_id = request.data.get("tran_id").split('_')[1]
    deposit = Deposit.objects.get(id=deposit_id)
    deposit.status = "failed"
    deposit.save()
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/deposit")


@api_view(['POST'])
def payment_fail(request):
    deposit_id = request.data.get("tran_id").split('_')[1]
    deposit = Deposit.objects.get(id=deposit_id)
    deposit.status = "failed"
    deposit.save()
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/deposit")