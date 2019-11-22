from api.product.serializers import ProcessorSerializer, RamMemorySerializer, MotherBoardSerializer, \
    VideoBoardSerializer
from orders.models import Order
from rest_framework.serializers import ModelSerializer


class OrderSerializer(ModelSerializer):
    processor = ProcessorSerializer(many=False)
    ramMemory = RamMemorySerializer(many=True)
    motherBoard = MotherBoardSerializer(many=False)
    videoBoard = VideoBoardSerializer(many=False)

    class Meta:
        model = Order
        fields = ('email', 'processor','ramMemory', 'motherBoard', 'videoBoard',)
