from products.models import Processor, RamMemory, MotherBoard, VideoBoard
from rest_framework.serializers import ModelSerializer


class ProcessorSerializer(ModelSerializer):
    class Meta:
        model = Processor
        fields = ('product',)


class RamMemorySerializer(ModelSerializer):
    class Meta:
        model = RamMemory
        fields = ('product', 'size',)


class MotherBoardSerializer(ModelSerializer):
    class Meta:
        model = MotherBoard
        fields = ('product',)


class VideoBoardSerializer(ModelSerializer):
    class Meta:
        model = VideoBoard
        fields = ('product',)
