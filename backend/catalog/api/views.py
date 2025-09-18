from rest_framework import generics
from rest_framework.response import Response
from catalog.models import Product, ProductVariant, AttributeValue
from .serializers import ProductSerializer, ProductVariantSerializer, AttributeValueSerializer
from rest_framework import generics
from catalog.models import Category
from .serializers import CategoryAttributesSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'



class ProductVariantListAPIView(generics.ListAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer



class ProductVariantDetailAPIView(generics.RetrieveAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    lookup_field = 'pk'



class AttributeValueListAPIView(generics.ListAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer



class ProductVariantsByProductAPIView(generics.ListAPIView):
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return ProductVariant.objects.filter(product_id=product_id)



class CategoryAttributesAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAttributesSerializer
    lookup_field = 'id'
    
    
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAttributesSerializer