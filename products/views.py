from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from . import models
# Create your views here.


class ProductsListView(ListView):
    model = models.Product


class ProductsDetailView(DetailView):
    model = models.Product

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.prefetch_related('similar_products')


class SubmitOrderView(View):
    def post(self, request, *args, **kwargs):
        print(request.body)
        # TODO: save order
        return JsonResponse({
    'status': 'ok',
    'text': 'Ваш заказ оформлен и мы вам напишем в течении трёх часов.'
    })
