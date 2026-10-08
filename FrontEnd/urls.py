from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('login/', views.login, name='login'),
    path('viaje/<int:pk>/', views.detalle_viaje, name='detalle_viaje'),
    path('viajes/nuevo/', views.form_viaje, name='form_viaje'),
    path('viajes/<int:pk>/editar/', views.form_viaje, name='editar_viaje'),
    path('personas/', views.personas, name='personas'),
    path('personas/nueva/', views.form_persona, name='form_persona'),
    path('personas/<int:pk>/editar/', views.form_persona, name='editar_persona'),
    path('lugares/', views.lugares, name='lugares'),
    path('lugares/nuevo/', views.form_lugar, name='form_lugar'),
    path('lugares/<int:pk>/editar/', views.form_lugar, name='editar_lugar'),
]