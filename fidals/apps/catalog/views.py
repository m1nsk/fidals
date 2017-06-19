from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

class ParamException(Exception):
    pass

class CatalogFilteredList(ListView):
    context_object_name = 'object_list'
    template_name = 'catalog_list.html'

    def get_queryset(self):
        ANY_OR_ALL = False
        offset, limit = 0, 0
        categories = []
        products = []
        try:
            if self.request.GET.get('categories'):
                categories = self.request.GET['categories'].split(',')
                for category in categories:
                    category = int(category)
                    if category < 0:
                        raise ParamException
            if self.request.GET.get('offset'):
                offset = int(self.request.GET['offset'])
                if offset < 0:
                    raise ParamException
            if self.request.GET.get('limit'):
                limit = int(self.request.GET['limit'])
                if limit < 0:
                    raise ParamException
        except (ValueError, ParamException) as e:
            return []

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
        return products
