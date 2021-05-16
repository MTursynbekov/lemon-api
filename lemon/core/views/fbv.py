from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import City, Product
from ..serializers import CitySerializer, ProductReadSerializer


@api_view(['GET', 'POST'])
def cities_list(request):
    if request.method == 'GET':
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
def get_city(request, pk):
    try:
        city = City.objects.get(id=pk)
    except City.DoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CitySerializer(instance=city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        city.delete()
        return Response({'deleted': True}, status=status.HTTP_200_OK)


@api_view(['GET', ])
def get_city_products(request, pk):
    if request.method == 'GET':
        city_products = Product.objects.get_by_city(city_id=pk)
        serializer = ProductReadSerializer(city_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
