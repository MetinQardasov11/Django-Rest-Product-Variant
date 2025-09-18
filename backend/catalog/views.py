from django.shortcuts import render, get_object_or_404, redirect
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, "catalog/product_list.html", {"products": products})

def product_variant_attributes(product):
    attrs = set()
    for v in product.variants.all():
        for av in v.attributes.all():
            attrs.add(av.attribute)
    return attrs


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    variants = product.variants.prefetch_related('attributes__attribute').all()

    variant_data = {}
    for v in variants:
        attrs = {val.attribute.name: val.value for val in v.attributes.all()}
        variant_data[v.id] = {
            'id': v.id,
            'sku': v.sku,
            'price': str(v.price),
            'stock': v.stock,
            'attributes': attrs,
        }

    attr_dict = {}
    for v in variants:
        for val in v.attributes.all():
            attr_dict.setdefault(val.attribute.name, set()).add(val.value)

    # 🔑 Burada sort edirik
    attr_dict = {
        k: sorted(
            (list(v)),          # əvvəlcə list-ə çevir
            key=lambda x: int(x) if x.isdigit() else x
        )
        for k, v in attr_dict.items()
    }

    default_variant = next(
        (v for v in variants if v.stock > 0),
        variants[0] if variants else None
    )

    return render(
        request,
        'catalog/product_detail.html',
        {
            'product': product,
            'variant_data': variant_data,
            'attributes': attr_dict,
            'default_variant': default_variant,
        }
    )
