from orders.models import Order
from rest_framework.serializers import ModelSerializer


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        depth = 3
        fields = '__all__'
