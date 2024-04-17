from django.shortcuts import render


from rest_framework.response import Response

from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,ListCreateAPIView,UpdateAPIView,DestroyAPIView

from rest_framework import authentication,permissions

from rest_framework.decorators import action

from rest_framework.views import APIView

from shop.serializers import UserSerializer,ProductSerializer,BasketSerializer,BasketItemSerializer

from shop.models import Product,Size,BasketItem,Order

from django.contrib.auth.models import User

KEY_ID="rzp_test_WecYy5jFmpezFY"

KEY_SECRET="zZWllBZ7wXypuSrUILnUYB5C"


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






class CartListView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        qs=request.user.cart

        serializer_instance=BasketSerializer(qs)

        return Response(data=serializer_instance.data)



class CartItemUpdateView(UpdateAPIView,DestroyAPIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    serializer_class=BasketItemSerializer

    queryset=BasketItem.objects.all()

    def perform_update(self, serializer):

        size_name=self.request.data.get("size_object")#L,M

        size_obj=Size.objects.get(name=size_name)


        serializer.save(size_object=size_obj)



    
class CheckOutView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):

        uesr_obj=request.user

        delivery_address=request.data.get("delivery_address")

        phone=request.data.get("phone")

        pin=request.data.get("pin")

        email=request.data.get("email")

        payment_mode=request.data.get("payment_mode")

        order_instance=Order.objects.create(

            user_object=uesr_obj,
            delivery_address=delivery_address,
            phone=phone,
            pin=pin,
            email=email,
            payment_mode=payment_mode
            
            )
        
        cart_items=request.user.cart.basketitems

        for bi in cart_items:
            order_instance.basket_item_objects.add(bi)
            bi.is_order_placed=True
            bi.save()

        order_instance.save()        

        return Response(data={"message":"created"})
    




        
      
            



        















        

