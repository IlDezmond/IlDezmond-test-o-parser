from rest_framework import serializers

from products.models import Product


class ProductReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductWriteSerializer(serializers.Serializer):
    products_count = serializers.IntegerField(
        min_value=1,
        max_value=50,
    )

    class Meta:
        model = Product
        fields = (
            'products_count',
        )
