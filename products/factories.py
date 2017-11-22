import factory
from factory import fuzzy

from . import models

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    title = factory.Faker('word')
    description = factory.Faker('sentence')
    is_published = factory.fuzzy.FuzzyChoice(choices = [True, False])
    image = factory.django.ImageField()
    category = models.Category.objects.all().first()