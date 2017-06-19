from django.conf.urls import url
from django.conf.urls import url, include
from django.conf import settings
from .api import CategoryViewSet, ProductViewSet, CatalogList, CatalogViewSet
from .views import CatalogFilteredList
from rest_framework.routers import DefaultRouter


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'catalog', CatalogViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^catalog_list/', CatalogList.as_view()),
    url(r'^catalog_filtered_list/', CatalogFilteredList.as_view()),
]
