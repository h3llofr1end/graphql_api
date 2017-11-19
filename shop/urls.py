from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from graphene_django.views import GraphQLView
from shop.schema import schema
from products import views as product_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    url(r'^products/$', product_views.ProductsListView.as_view()),
    url(
        r'^products/(?P<pk>[0-9]+)/',
        product_views.ProductsDetailView.as_view(),
        name='product_detail'
    ),
]  \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
