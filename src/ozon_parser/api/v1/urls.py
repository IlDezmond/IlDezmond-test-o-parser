from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import ProductViewSet

router_v1 = DefaultRouter()

router_v1.register('products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(router_v1.urls)),
]
