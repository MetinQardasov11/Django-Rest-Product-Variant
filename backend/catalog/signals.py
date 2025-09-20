from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
from catalog.models import ProductVariant


def custom_slugify(text):
    replacements = {'ə': 'e', 'ç': 'c', 'ş': 's', 'ğ': 'g', 'ü': 'u', 'ö': 'o', 'ı': 'i', 'İ': 'i', 'Ə': 'E', 'Ç': 'C', 'Ş': 'S', 'Ğ': 'G', 'Ü': 'U', 'Ö': 'O', }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return slugify(text)

@receiver(m2m_changed, sender=ProductVariant.attributes.through)
def update_variant_slug(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        attr_values = instance.attributes.all().order_by('attribute__name')
        if not attr_values:
            return

        attr_slug_parts = [f"{custom_slugify(av.attribute.name)}-{custom_slugify(av.value)}" for av in attr_values]
        attr_str = "-".join(attr_slug_parts)
        base_slug = f"{custom_slugify(instance.product.name)}-{attr_str}"
        slug = base_slug
        counter = 1
        while ProductVariant.objects.filter(slug=slug).exclude(id=instance.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        ProductVariant.objects.filter(id=instance.id).update(slug=slug)