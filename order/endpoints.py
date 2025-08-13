from drf_yasg.utils import swagger_auto_schema
from order.serializers import UpdateOrderSerializer, CartItemSerializer,CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, WishlistSerializer

class OrderEndpoints:
    list = swagger_auto_schema(
        operation_summary="Retrieve list of orders",
        operation_description=(
            "Admins see all orders. Sellers see orders of their product. Users see only their own orders. "
            "Includes order items and product details."
        )
    )
    
    retrieve = swagger_auto_schema(
        operation_summary="Get details of a specific order",
        operation_description=(
            "Accessible by order owner, sellers (if product belongs to them), and admins. "
            "Shows full order info including items."
        )
    )
    
    create = swagger_auto_schema(
        operation_summary="Place a new order from a cart",
        operation_description=(
            "Requires authenticated user. Validates cart and user address. "
            "Creates order and empties cart."
        )
    )
    
    cancel = swagger_auto_schema(
        methods=['post'],
        operation_summary="Cancel an order",
        operation_description=(
            "Users can cancel only their own orders. Admins can cancel any order. "
            "Cannot cancel delivered orders."
        ),
        responses={200: 'Order canceled'}
    )
    
    update_status = swagger_auto_schema(
        methods=['patch'],
        operation_summary="Admin updates order status",
        operation_description="Only admins can update status like processing, shipped, delivered.",
        request_body=UpdateOrderSerializer,
        responses={200: 'Order status updated'}
    )
    
    destroy = swagger_auto_schema(
        operation_summary="Delete an order",
        operation_description="Only admins can delete orders."
    )



class CartEndpoints:
    list = swagger_auto_schema(
        operation_summary="Retrieve Cart",
        operation_description="Returns all items currently in the logged-in user's cart along with total price and quantity.",
        responses={200: CartSerializer}
    )

    list_items = swagger_auto_schema(
        operation_summary="List Cart Items",
        operation_description="Lists all items in the specified cart, including product details, price, and quantity.",
        responses={200: CartItemSerializer(many=True)}
    )

    retrieve_item = swagger_auto_schema(
        operation_summary="Retrieve Cart Item",
        operation_description="Get detailed information for a specific cart item in the specified cart.",
        responses={200: CartItemSerializer}
    )

    add = swagger_auto_schema(
        operation_summary="Add Item to Cart",
        operation_description="Adds a specified product to the cart. If the product already exists, increase the quantity.",
        request_body=AddCartItemSerializer,
        responses={201: CartItemSerializer}
    )

    update = swagger_auto_schema(
        operation_summary="Update Cart Item",
        operation_description="Update the quantity of a specific cart item. Quantity must be at least 1.",
        request_body=UpdateCartItemSerializer,
        responses={200: CartItemSerializer}
    )

    remove = swagger_auto_schema(
        operation_summary="Remove Cart Item",
        operation_description="Removes a product from the user's cart.",
        responses={204: 'No Content'}
    )

class WishlistEndpoints:
    list = swagger_auto_schema(
        operation_summary="List Wishlist Items",
        operation_description="Retrieve all items in the logged-in user's wishlist.",
        responses={200: WishlistSerializer(many=True)}
    )

    retrieve = swagger_auto_schema(
        operation_summary="Retrieve Wishlist Item",
        operation_description="Retrieve details of a specific wishlist item.",
        responses={200: WishlistSerializer}
    )

    create = swagger_auto_schema(
        operation_summary="Add to Wishlist",
        operation_description="Add a new product to the logged-in user's wishlist.",
        request_body=WishlistSerializer,
        responses={201: WishlistSerializer}
    )

    update = swagger_auto_schema(
    operation_summary="Update Wishlist Item",
    operation_description="Update details of a wishlist item. User can update their own wishlist.",
    request_body=WishlistSerializer,
    responses={200: WishlistSerializer}
    )

    remove = swagger_auto_schema(
        operation_summary="Remove from Wishlist",
        operation_description="Delete an item from the logged-in user's wishlist.",
        responses={204: 'No Content'}
    )

