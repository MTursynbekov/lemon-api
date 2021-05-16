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


class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ('id', 'src',)


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSpecification
        fields = ('key', 'value')


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('name', 'price', 'discount', 'category_id')
        extra_kwargs = {
            'category_id': {'write_only': True},
        }

    def validate(self, attr):
        if attr['publication_date'] > attr['discount_ends_date']:
            raise serializers.ValidationError("discount must end after publication date")
        return attr


class ProductReadSerializer(ProductWriteSerializer):
    category = CategorySerializer()
    city = CitySerializer()
    brand = BrandSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        fields = ProductWriteSerializer.Meta.fields + ('price_ with_discount', 'city', 'category', 'brand', 'images')


class ProductFullSerializer(ProductReadSerializer):
    stores = StoreSerializers()
    specifications = ProductSpecificationSerializer(many=True)

    class Meta:
        fields = '__all__'
