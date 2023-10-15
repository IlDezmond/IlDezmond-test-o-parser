from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from products.models import Product
from .serializers import ProductReadSerializer, ProductWriteSerializer


class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductWriteSerializer
        return ProductReadSerializer

    def create(self, request, *args, **kwargs):
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_count = serializer.validated_data.get('products_count')
        print(product_count)
        # parse(product_count).delay()
        return Response(status=status.HTTP_201_CREATED)

