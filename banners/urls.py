from django.urls import path
from .views import BannerList,BannerDetail


urlpatterns = [
    path('', BannerList.as_view()),
    path('<str:slug>/', BannerDetail.as_view()),
]
