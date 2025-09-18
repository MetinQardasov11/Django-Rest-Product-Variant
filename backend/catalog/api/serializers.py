from rest_framework import serializers
from catalog.models import Product, ProductVariant, AttributeValue

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute_name', 'value']


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku', 'price', 'stock', 'attributes']
        
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
