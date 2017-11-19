from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import models
# Create your views here.


class ProductsListView(ListView):
    model = models.Product


class ProductsDetailView(DetailView):
    model = models.Product