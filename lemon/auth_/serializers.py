from rest_framework import serializers

from auth_ import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        exclude = ('user',)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainUser
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = models.MainUser.objects.create_user(email=validated_data['email'],
                                                   password=validated_data['password'])
        user.save()
        return user


class UserSerializer(UserCreateSerializer):
    profile = ProfileSerializer()

    class Meta(UserCreateSerializer.Meta):
        fields = ('id', 'profile') + UserCreateSerializer.Meta.fields

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.role = validated_data.get('role', instance.role)
        profile.address = profile_data.get('address', profile.address)
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.birth_date = profile_data.get('birth_date', profile.birth_date)
        profile.save()
        instance.save()
        return instance


