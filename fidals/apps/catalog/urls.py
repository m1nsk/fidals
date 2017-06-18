from django.conf.urls import url
from django.conf.urls import url, include
from django.conf import settings
from .views import CategoryViewSet, ProductViewSet, CatalogList
from rest_framework.routers import DefaultRouter


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^catalog/', CatalogList.as_view()),
]
