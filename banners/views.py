from django.shortcuts import render
from .models import Banner
from .serializers import BannerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status


class BannerList(APIView):
    def get(self,request, format=None):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True,context={'request':request})
        return Response(serializer.data)
# Create your views here.


class BannerDetail(APIView):
    def get_object(self,slug):
        try:
            return Banner.objects.get(slug=slug)
        except Banner.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        banner = self.get_object(slug)
        serializer = BannerSerializer(banner,context={'request':request})
        return Response(serializer.data)

    def put(self,request, slug, format =None):
        banner = self.get_object(slug)
        serializer = BannerSerializer(banner, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, slug, format=None):
        banner = self.get_object(slug)
        banner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


