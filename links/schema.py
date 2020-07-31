import graphene
from graphene_django  import DjangoObjectType

from .models import Link, Vote
from users.schema import UserType
from graphql import GraphQLError
from django.db.models import Q

# os types criadas por mim,herdam de DjangoObjectType e 
# deve have um type para cada model criada por mim

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

#graphene.ObjectType para queries
class Query(graphene.ObjectType):
    links = graphene.List(
        LinkType, 
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = graphene.List(VoteType)


    #cada query precisa ter um resolver dizendo o que acontece
    def resolve_links(self, info, search=None,first=None,skip=None, **kwargs):
        qs = Link.objects.all()
        if search:
            filter = (
                Q(url__icontains=search)|
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
            
        return qs
    
    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

#graphene.Mutation para escritas, mutations
class CreateLink(graphene.Mutation):
    # preciso passar o tipo que eu vou receber nas mutations
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    #essa classe Arguments é o que eu vou receber do client.
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #aqui eu faço a relação do que ta vindo do client, com o objeto que vai pro banco, eu monto
    # o objeto.Pra isso que serve essa função mutate.
    def mutate(self, info, url, description):
        user = info.context.user or None
        
        link = Link(
            url=url,
            description=description,
            posted_by=user,
        )
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user or None
        if user.is_anonymous:
            raise GraphQLError('you must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user = user,
            link = link,
        )

        return CreateVote(user=user, link=link)

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()