from django.http import JsonResponse
from django.templatetags.static import static
from .models import Order, OrderItem
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .serializers import OrderSerializer, OrderItemSerializer
from django.core import serializers


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()
    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


# class OrderItemSerializer(ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['product', 'quantity']
#
#
# class OrderSerializer(ModelSerializer):
#     products = OrderItemSerializer(many=True, allow_empty=False, write_only=True)
#
#     class Meta:
#         model = Order
#         fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']


@api_view(['POST'])
def register_order(request):
    serializer_order = OrderSerializer(data=request.data)
    serializer_order.is_valid(raise_exception=True)
    products = request.data.get('products', [])
    my_order = Order.objects.create(
        firstname=serializer_order.validated_data['firstname'],
        lastname=serializer_order.validated_data['lastname'],
        phonenumber=serializer_order.validated_data['phonenumber'],
        address=serializer_order.validated_data['address']
    )
    for order in products:
        serializer = OrderItemSerializer(data=order)
        serializer.is_valid(raise_exception=True)
        OrderItem.objects.create(
            product=serializer.validated_data['product'],
            order=my_order,
            quantity=serializer.validated_data['quantity'],
            price=serializer.validated_data['product'].price * serializer.validated_data['quantity'],

        )
    return Response(OrderSerializer(my_order).data)








    # try:
    #     print(serialized_order.keys())
    #     if isinstance(serialized_order['products'], list) and serialized_order['products']:
    #         try:
    #             if serialized_order['firstname']:
    #                 my_order = Order.objects.create(first_name=serialized_order['firstname'],
    #                                                 last_name=serialized_order['lastname'],
    #                                                 phone_number=serialized_order['phonenumber'],
    #                                                 address=serialized_order['address'])
    #
    #             else:
    #                 content_error = {'firstname': 'Это поле не может быть пустым.'}
    #                 return Response(content_error, status=status.HTTP_400_BAD_REQUEST)
    #             if serialized_order.keys():
    #                 my_order = Order.objects.create(first_name=serialized_order['firstname'],
    #                                                 last_name=serialized_order['lastname'],
    #                                                 phone_number=serialized_order['phonenumber'],
    #                                                 address=serialized_order['address'])
    #
    #             else:
    #                 content_error = {'firstname, lastname, phonenumber, address': 'Это поле не может быть пустым.'}
    #                 return Response(content_error, status=status.HTTP_400_BAD_REQUEST)
    #         except KeyError:
    #             key_error = {'firstname, lastname, phonenumber, address': 'Обязательное поле'}
    #             return Response(key_error, status=status.HTTP_400_BAD_REQUEST)
    #         for order in serialized_order['products']:
    #             OrderItem.objects.create(product=Product.objects.get(pk=order['product']),
    #                                      order=my_order,
    #                                      quantity=order['quantity'])
    #         return Response(serialized_order, status=status.HTTP_200_OK)
    #     else:
    #         content_error = {'products': 'Это поле не может быть строкой или пустым.'}
    #         return Response(content_error, status=status.HTTP_400_BAD_REQUEST)
    # except KeyError:
    #     key_error = {'products': 'Обязательное поле.'}
    #     return Response(key_error, status=status.HTTP_400_BAD_REQUEST)
