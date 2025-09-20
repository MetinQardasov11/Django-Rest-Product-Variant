from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductVariantListAPIView,
    ProductVariantDetailAPIView,
    AttributeValueListAPIView,
    ProductVariantsByProductAPIView,
    CategoryAttributesAPIView,
    CategoryListAPIView, 
    WishlistListCreateAPIView, 
    WishlistDeleteAPIView
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('products/<int:pk>/variants/', ProductVariantsByProductAPIView.as_view(), name='api-product-variants'),
    path('variants/', ProductVariantListAPIView.as_view(), name='api-variant-list'),
    path('variants/<slug:slug>/', ProductVariantDetailAPIView.as_view(), name='api-variant-detail'),
    path('attributes/', AttributeValueListAPIView.as_view(), name='api-attribute-list'),
    path('category/<int:id>/attributes/', CategoryAttributesAPIView.as_view(), name='category-attributes'),
    path('categories/', CategoryListAPIView.as_view(), name='api-category-list'),
    path("wishlist/", WishlistListCreateAPIView.as_view(), name="wishlist-list-create"),
    path("wishlist/<int:pk>/", WishlistDeleteAPIView.as_view(), name="wishlist-delete"),
]