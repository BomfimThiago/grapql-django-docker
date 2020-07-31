from django.contrib import admin
from django.urls import path
#preciso desativar esse csrf para usar o graphqi, a interface do graphql
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]
