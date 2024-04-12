from django.contrib.auth.models import User

from rest_framework import serializers

from shop.models import Product,Category,Brand,Size

class UserSerializer(serializers.ModelSerializer):

    password1=serializers.CharField(write_only=True)

    password2=serializers.CharField(write_only=True)

    class Meta:

        model=User

        fields=["id","username","email","password1","password2","password"]

        read_only_fields=["id","password"]

    def create(self, validated_data):

        password1=validated_data.pop("password1")

        password2=validated_data.pop("password2")

        if password1 != password2:

            raise serializers.ValidationError("password not same")
        else:
            return User.objects.create_user(**validated_data,password=password2)
        
    



class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model=Category

        fields=["id","name"]


class BrandSerializer(serializers.ModelSerializer):

    class Meta:

        model=Brand

        fields=["id","name"]


class SizeSerializer(serializers.ModelSerializer):

    class Meta:

        model=Size

        fields=["id","name"]



class ProductSerializer(serializers.ModelSerializer):

    category_object=CategorySerializer(read_only=True)

    brand_object=BrandSerializer(read_only=True)

    size_object=SizeSerializer(read_only=True,many=True)

    # category_object=serializers.StringRelatedField(read_only=True)

    class Meta:

        model=Product

        fields="__all__"
