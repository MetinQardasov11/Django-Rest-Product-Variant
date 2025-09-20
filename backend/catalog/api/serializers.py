from rest_framework import serializers
from catalog.models import Product, ProductVariant, AttributeValue, Category, Wishlist

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute_name', 'value']


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'slug', 'sku', 'price', 'stock', 'attributes']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        attr_dict = {}
        for a in data['attributes']:
            attr_dict.setdefault(a['attribute_name'], []).append(a['value'])
        
        for k, v in attr_dict.items():
            attr_dict[k] = sorted(v, key=lambda x: int(x) if x.isdigit() else x)
        
        data['attributes_grouped'] = attr_dict
        return data


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'image', 'variants']


class CategoryAttributesSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'attributes']

    def get_attributes(self, obj):
        variants = ProductVariant.objects.filter(product__category__in=obj.get_descendants(include_self=True)).prefetch_related('attributes__attribute')
        
        attr_dict = {}
        for variant in variants:
            for av in variant.attributes.all():
                attr_dict.setdefault(av.attribute.name, set()).add(av.value)

        for k in attr_dict:
            try:
                attr_dict[k] = sorted(attr_dict[k], key=lambda x: float(x))
            except ValueError:
                attr_dict[k] = sorted(attr_dict[k])
        return attr_dict
    
    
class WishlistSerializer(serializers.ModelSerializer):
    variant_detail = ProductVariantSerializer(source="variant", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "variant", "variant_detail", "created_at"]
        read_only_fields = ["id", "created_at"]