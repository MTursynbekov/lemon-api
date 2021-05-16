from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from ..models import Product, Category, Brand, Promotion, Store, ProductImage, ProductSpecification
from core import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'delete':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=True, url_path='products')
    def category_products(self, request, pk):
        category_products = Product.objects.get_by_category(category_id=pk)
        serializer = serializers.ProductReadSerializer(category_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandsListAPIView(APIView):
    def get_permissions(self):
        if self.request.method.lower() == 'post':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get(self, request):
        products = Brand.objects.all()
        serializer = serializers.BrandSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BrandDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method.lower() == 'get':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_object(self, id):
        try:
            return Brand.objects.get(id=id)
        except Brand.DoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        products = Product.objects.get_by_brand(brand_id=pk)
        serializer = serializers.ProductReadSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        brand = self.get_object(pk)
        serializer = serializers.BrandSerializer(instance=brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors})

    def delete(self, request, pk):
        brand = self.get_object(pk)
        brand.delete()
        return Response({'deleted': True})


class BrandsPromotionsAPIView(APIView):
    def get(self, request, pk):
        promotions = Promotion.objects.get_by_brand(brand_id=pk)
        serializer = serializers.PromotionReadSerializer(promotions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"deleted": True}, status=status.HTTP_204_NO_CONTENT)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = serializers.PromotionReadSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.PromotionCreateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductReadSerializer

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.ProductWriteSerializer
        elif self.action == 'retrieve':
            return serializers.ProductFullSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ProductImageViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageCreateSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsAdminUser, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"deleted": True}, status=status.HTTP_204_NO_CONTENT)


class ProductSpecificationViewSet(viewsets.GenericViewSet,
                                  mixins.CreateModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = ProductSpecification.objects.all()
    serializer_class = serializers.ProductSpecificationSerializer
    permission_classes = [IsAdminUser, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"deleted": True}, status=status.HTTP_204_NO_CONTENT)
