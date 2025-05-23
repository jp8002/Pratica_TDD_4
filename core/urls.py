from django.urls import path
from core.views import login, logout, home, cadastrar, listar, editar, excluir

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home,name='home'),
    path("cadastrar/", cadastrar,name="cadastrar"),
    path("listar/", listar,name="listar"),
    path("editar/", editar, name="editar"),
    path("editar/<int:id>", editar, name="editar"),
    path("excluir/", excluir, name="excluir"),
]