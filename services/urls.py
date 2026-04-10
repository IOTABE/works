from django.urls import path
from .views import (
    home, create_offer, create_request, my_services, delete_service,
    category_list, category_create, category_update, category_delete
)

urlpatterns = [
    path('', home, name='home'),
    path('anunciar/', create_offer, name='create_offer'),
    path('pedir/', create_request, name='create_request'),
    path('meus-anuncios/', my_services, name='my_services'),
    path('excluir-anuncio/<int:pk>/<str:type_service>/', delete_service, name='delete_service'),
    
    # Gerenciamento de Categorias
    path('categorias/', category_list, name='category_list'),
    path('categorias/nova/', category_create, name='category_create'),
    path('categorias/editar/<int:pk>/', category_update, name='category_update'),
    path('categorias/excluir/<int:pk>/', category_delete, name='category_delete'),
]
