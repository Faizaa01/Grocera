from drf_yasg.utils import swagger_auto_schema
from product.serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ReviewSerializer


class ProductEndpoints:
    list = swagger_auto_schema(
        operation_summary="List Products",
        operation_description="Retrieve a list of all products. Supports search, ordering, and filtering by category.",
        responses={200: ProductSerializer(many=True)}
    )

    retrieve = swagger_auto_schema(
        operation_summary="Retrieve Product",
        operation_description="Retrieve details of a specific product by ID.",
        responses={200: ProductSerializer}
    )

    create = swagger_auto_schema(
        operation_summary="Create Product",
        operation_description="Create a new product. Seller or admin only.",
        request_body=ProductSerializer,
        responses={201: ProductSerializer}
    )

    update = swagger_auto_schema(
        operation_summary="Update Product",
        operation_description="Update an existing product. Seller or admin only.",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )

    remove = swagger_auto_schema(
        operation_summary="Delete Product",
        operation_description="Delete a product. Seller or admin only.",
        responses={204: 'No Content'}
    )

class ProductImageEndpoints:
    list = swagger_auto_schema(
        operation_summary="List Product Images",
        operation_description="Retrieve all images for the specified product.",
        responses={200: ProductImageSerializer(many=True)}
    )

    retrieve = swagger_auto_schema(
        operation_summary="Retrieve Product Image",
        operation_description="Retrieve a specific product image by ID.",
        responses={200: ProductImageSerializer}
    )

    create = swagger_auto_schema(
        operation_summary="Add Product Image",
        operation_description="Add a new image to the specified product. Only the product's seller or admin can add images.",
        request_body=ProductImageSerializer,
        responses={201: ProductImageSerializer}
    )

    update = swagger_auto_schema(
        operation_summary="Update Product Image",
        operation_description="Update a product image. Only the product's seller or admin can update images.",
        request_body=ProductImageSerializer,
        responses={200: ProductImageSerializer}
    )

    remove = swagger_auto_schema(
        operation_summary="Delete Product Image",
        operation_description="Delete a product image. Only the product's seller or admin can delete images.",
        responses={204: 'No Content'}
    )


class CategoryEndpoints:
    list = swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="Retrieve all categories along with the number of products in each.",
        responses={200: CategorySerializer(many=True)}
    )

    retrieve = swagger_auto_schema(
        operation_summary="Retrieve Category",
        operation_description="Retrieve details of a specific category including product count.",
        responses={200: CategorySerializer}
    )

    create = swagger_auto_schema(
        operation_summary="Create Category",
        operation_description="Create a new product category. Admin only.",
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )

    update = swagger_auto_schema(
        operation_summary="Update Category",
        operation_description="Update details of an existing category. Admin only.",
        request_body=CategorySerializer,
        responses={200: CategorySerializer}
    )

    remove = swagger_auto_schema(
        operation_summary="Delete Category",
        operation_description="Delete an existing category. Admin only.",
        responses={204: 'No Content'}
    )

    

class ReviewEndpoints:
    list = swagger_auto_schema(
        operation_summary="List Reviews",
        operation_description="Retrieve all reviews for a specific product. Supports pagination.",
        responses={200: ReviewSerializer(many=True)}
    )

    retrieve = swagger_auto_schema(
        operation_summary="Retrieve Review",
        operation_description="Retrieve details of a specific review by ID.",
        responses={200: ReviewSerializer}
    )

    create = swagger_auto_schema(
        operation_summary="Create Review",
        operation_description="Create a new review for the specified product.",
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer}
    )

    update = swagger_auto_schema(
        operation_summary="Update Review",
        operation_description="Update a review. Only the owner or admin can update.",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer}
    )

    partial_update = swagger_auto_schema(
        operation_summary="Partial Update Review",
        operation_description="Partially update a review. Only the owner or admin can update.",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer}
    )

    remove = swagger_auto_schema(
        operation_summary="Delete Review",
        operation_description="Delete a review. Only the owner or admin can delete.",
        responses={204: 'No Content'}
    )
