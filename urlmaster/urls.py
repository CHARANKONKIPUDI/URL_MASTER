from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("result/", views.result, name="result"),
    path("qr-code/", views.qr_code_view, name="qr_code"),
    path("s/<str:code>/", views.redirect_short, name="redirect_short"),
]
