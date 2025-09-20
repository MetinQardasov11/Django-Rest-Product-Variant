from typing import Iterable
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()



class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name="Kateqoriya Adı")
    image = models.ImageField(upload_to='category_images/', verbose_name="Kateqoriya Resmi")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Üst Kateqoriya")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True, blank=True, verbose_name="Slug")


    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = "Məhsul Kategoriyaları"
    
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)


    def get_all_products(self):
        descendants = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=descendants)

    @property
    def total_products_count(self):
        return self.get_all_products().count()


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[str(self.id)])


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    attributes = models.ManyToManyField(AttributeValue, related_name="variants")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True, verbose_name="Slug")

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "variant")

    def __str__(self):
        attr_pairs = self.variant.attributes.values_list("attribute__name", "value")
        if attr_pairs:
            attrs = ", ".join(f"{name}:{value}" for name, value in attr_pairs)
            return f"{self.user.username} -> {self.variant.product.name} - {self.variant.sku} ({attrs})"
        return f"{self.user.username} -> {self.variant.product.name} - {self.variant.sku}"
