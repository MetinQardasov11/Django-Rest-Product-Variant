from rest_framework import generics
from rest_framework.response import Response
from catalog.models import Product, ProductVariant, AttributeValue
from .serializers import ProductSerializer, ProductVariantSerializer, AttributeValueSerializer, WishlistSerializer, CategoryAttributesSerializer
from rest_framework import generics
from catalog.models import Category, Wishlist
from rest_framework import permissions

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.AllowAny]



class ProductVariantListAPIView(generics.ListAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny]



class ProductVariantDetailAPIView(generics.RetrieveAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]



class AttributeValueListAPIView(generics.ListAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = [permissions.AllowAny]



class ProductVariantsByProductAPIView(generics.ListAPIView):
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return ProductVariant.objects.filter(product_id=product_id)



class CategoryAttributesAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAttributesSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]
    
    
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryAttributesSerializer
    permission_classes = [permissions.AllowAny]
    
    
class WishlistListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistDeleteAPIView(generics.DestroyAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)