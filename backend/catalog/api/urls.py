from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductVariantListAPIView,
    ProductVariantDetailAPIView,
    AttributeValueListAPIView,
    ProductVariantsByProductAPIView,
)

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='api-product-list'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('products/<int:pk>/variants/', ProductVariantsByProductAPIView.as_view(), name='api-product-variants'),
    path('variants/', ProductVariantListAPIView.as_view(), name='api-variant-list'),
    path('variants/<int:pk>/', ProductVariantDetailAPIView.as_view(), name='api-variant-detail'),
    path('attributes/', AttributeValueListAPIView.as_view(), name='api-attribute-list'),
]