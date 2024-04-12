from django.shortcuts import render


from rest_framework.response import Response

from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,ListCreateAPIView

from rest_framework import authentication,permissions

from rest_framework.decorators import action

from rest_framework.views import APIView

from shop.serializers import UserSerializer,ProductSerializer

from shop.models import Product,Size,BasketItem

from django.contrib.auth.models import User


class SignUpView(CreateAPIView):

    serializer_class=UserSerializer

    queryset=User.objects.all()




class ProductListView(ListAPIView):

    serializer_class=ProductSerializer

    queryset=Product.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


class ProductDetailView(RetrieveAPIView):

    serializer_class=ProductSerializer

    queryset=Product.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]



# url:http://127.0.0.1:8000/api/v1/products/{id}/addtocart/

#         method:post

#         data:{

#             "size":"product size",
#             "quantity":"product quantitity",

#         }


class AddToCartView(APIView):

    permission_classes=[permissions.IsAuthenticated]

    authentication_classes=[authentication.TokenAuthentication]



    def post(self,request,*args,**kwargs):

        basket_object=request.user.cart

        id=kwargs.get("pk")

        product_object=Product.objects.get(id=id)

        size_name=request.data.get("size")

        size_object=Size.objects.get(name=size_name)

        quantity=request.data.get("quantity")

        BasketItem.objects.create(
            
            basket_object=basket_object,
            product_object=product_object,
            size_object=size_object,
            quantity=quantity
        )

        return Response(data={"message":"created"})













