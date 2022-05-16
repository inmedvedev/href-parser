from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.BaseView.as_view())
]
