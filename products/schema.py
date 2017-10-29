import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from products import models


class ProductType(DjangoObjectType):
    class Meta:
        model = models.Product
        filter_fields = {
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
        }
        interfaces = (graphene.relay.Node,)


class CategoryType(DjangoObjectType):
    class Meta:
        model = models.Category
        filter_fields = {
            'title': ['exact', 'icontains'],
        }
        interfaces = (graphene.relay.Node,)


class Query(graphene.AbstractType):
    products = DjangoFilterConnectionField(ProductType)
    category = DjangoFilterConnectionField(CategoryType)

    def resolve_products(self, info, **kwargs):
        return models.Product.objects.all()

    def resolve_category(self, info, **kwargs):
        return models.Category.objects.all()

class CreateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, title):
        models.Category(title=title).save()
        return CreateCategory(ok=True)