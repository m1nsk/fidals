from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
import json
from rest_framework import status
from .models import Category, Product
from rest_framework.views import APIView
from .serializers import CategorySerializer, ProductSerializer
from django.db.models import Count


class ParamException(Exception):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class CatalogList(APIView):
    def get(self, request, format=None):
        ANY_OR_ALL = False
        offset, limit = 0, 0
        categories = []
        products = []
        try:
            if request.query_params.get('categories'):
                categories = request.query_params['categories'].split(',')
                for category in categories:
                    category = int(category)
                    if category < 0:
                        raise ParamException
            if request.query_params.get('offset'):
                offset = int(request.query_params['offset'])
                if offset < 0:
                    raise ParamException
            if request.query_params.get('limit'):
                limit = int(request.query_params['limit'])
                if limit < 0:
                    raise ParamException
        except (ValueError, ParamException) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if categories:
            categories = list(set(categories))
            if ANY_OR_ALL:
                # matching ANY item in list:
                products = Product.objects.filter(categories__in=categories).distinct()
            else:
                # matching ALL items in list:
                candidate_products = Product.objects.filter(categories=categories.pop())
                for category in categories:
                    candidate_products = candidate_products.filter(categories=category)
                products = candidate_products
        else:
            products = Product.objects.all()

        if limit:
            if offset:
                products = products[offset: limit]
            else:
                products = products[:limit]
        else:
            if offset:
                products = products[offset:]

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



