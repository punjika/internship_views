from django.urls import path
from . import views

urlpatterns = [
    path('generate-graph/', views.generate_graph, name='generate_graph'),
]
