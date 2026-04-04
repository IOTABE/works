from django.urls import path
from .views import home, create_offer, create_request, my_services, delete_service

urlpatterns = [
    path('', home, name='home'),
    path('anunciar/', create_offer, name='create_offer'),
    path('pedir/', create_request, name='create_request'),
    path('meus-anuncios/', my_services, name='my_services'),
    path('excluir-anuncio/<int:pk>/<str:type_service>/', delete_service, name='delete_service'),
]
