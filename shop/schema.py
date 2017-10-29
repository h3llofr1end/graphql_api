import graphene

from products import schema as products_schema


class Query(products_schema.Query, graphene.ObjectType):
    pass

class Mutations(graphene.ObjectType):
    create_category = products_schema.CreateCategory.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)