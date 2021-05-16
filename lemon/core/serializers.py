from rest_framework import serializers

from core import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        category = models.City()
        category.name = validated_data.get('name')
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance


class BrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        category = models.Brand()
        category.name = validated_data.get('name')
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.save()
        return instance


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = '__all__'


class ProductImageCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.ProductImage
        fields = ('id', 'src', 'product_id')


class PromotionCreateSerializer(serializers.ModelSerializer):
    brand_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Promotion
        fields = ('src', 'start_date', 'finish_date', 'brand_id')

    def validate(self, attr):
        if attr['start_date'] > attr['finish_date']:
            raise serializers.ValidationError("end of promotion must occur after it starts")
        return attr


class PromotionReadSerializer(PromotionCreateSerializer):
    brand = BrandSerializer()

    class Meta(PromotionCreateSerializer.Meta):
        fields = ('id', 'brand') + PromotionCreateSerializer.Meta.fields


class ProductSpecificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.ProductSpecification
        fields = ('id', 'key', 'value', 'product_id')


class ProductWriteSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.Product
        fields = ('name', 'price', 'discount', 'category_id')


class ProductReadSerializer(ProductWriteSerializer):
    category = CategorySerializer()
    city = CitySerializer()
    brand = BrandSerializer()
    images = ProductImageCreateSerializer(many=True)
    id = serializers.IntegerField(read_only=True)

    class Meta(ProductWriteSerializer.Meta):
        fields = ('id',) + ProductWriteSerializer.Meta.fields + (
            'price_with_discount', 'city', 'category', 'brand', 'images')


class ProductFullSerializer(ProductReadSerializer):
    stores = StoreSerializer(many=True)
    specifications = ProductSpecificationSerializer(many=True)

    class Meta(ProductReadSerializer.Meta):
        fields = '__all__'
