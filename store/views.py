from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView 
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all() 

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context = {'request': request} )
        return Response(serializer.data) 

    def post(self, request):
         serializer = ProductSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)

        
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        Product = get_object_or_404(Product, pk=id)
        if Product.orderitems.count() > 0:
             return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HT