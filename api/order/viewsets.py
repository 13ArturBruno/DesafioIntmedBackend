from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.core.validators import validate_email

from api.order.serializers import OrderSerializer
from orders.models import Order
from products.models import Processor, RamMemory, MotherBoard, VideoBoard


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = [OrderSerializer, ]
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            email = request.data['email']
            processor = request.data['processor']
            ram_memory = request.data['ram_memory']
            mother_board = request.data['mother_board']
            video_board = request.data['video_board']
        except:
            return Response(data={"detail": "Ocorreu um erro ao captura os dados informados!"}, status=400)

        if email is None:
            return Response(data={"detail": "É necessário informar seu email para efetuar o pedido!"}, status=400)

        try:
            validate_email(email)
        except:
            return Response(data={"detail": "Email informado não é válido!"}, status=400)

        try:
            processor = Processor.objects.get(product=processor)
        except Processor.DoesNotExist:
            return Response(data={"detail": "Não foi possível encontrar o Processador especificado!"}, status=400)

        try:
            if ram_memory is None or len(ram_memory) == 0:
                return Response(data={'detail': "Nenhuma Memória Ram foi especificada!"},
                                status=400)

            for ram in ram_memory:
                memory = RamMemory.objects.get(size=ram)
        except RamMemory.DoesNotExist:
            return Response(data={'detail': "Não foi possível encontrar alguma das Memórias Ram especificada!"},
                            status=400)

        try:
            mother_board = MotherBoard.objects.get(product=mother_board)
        except MotherBoard.DoesNotExist:
            return Response(data={'detail': "Não foi possível encontrar a Placa Mãe especificada!"}, status=400)

        try:
            if mother_board.videoOnboard:
                if video_board is None:
                    pass
                else:
                    video_board = VideoBoard.objects.get(product=video_board)
            else:
                video_board = VideoBoard.objects.get(product=video_board)
        except VideoBoard.DoesNotExist:
            return Response(data={'detail': "Não foi possível encontrar o Placa de Video especificada!"}, status=400)

        if processor.brand in mother_board.cpuSupport.all():
            if len(ram_memory) <= mother_board.ramSlots:
                if sum(ram_memory) <= mother_board.maxMemorySize:
                    if video_board:
                        order = Order.objects.create(
                            email=email,
                            processor=processor,
                            motherBoard=mother_board,
                            videoBoard=video_board
                        )

                        for ram in ram_memory:
                            memory = RamMemory.objects.get(size=ram)
                            order.ramMemory.add(memory)

                        order.save()

                        return Response(
                            data={'message': "Pedido Criado Com Sucesso!"},
                            status=200)

                    else:
                        order = Order.objects.create(
                            email=email,
                            processor=processor,
                            motherBoard=mother_board,
                        )

                        for ram in ram_memory:
                            memory = RamMemory.objects.get(size=ram)
                            order.ramMemory.add(memory)

                        order.save()

                        return Response(
                            data={'message': "Pedido Criado Com Sucesso!"},
                            status=200)
                else:
                    return Response(
                        data={'detail': "Capacidade de Memória Ram para a Placa Mãe especificada foi excedida!"},
                        status=400)
            else:
                return Response(
                    data={'detail': "Limite de Slots para a Memória Ram para a Placa Mãe especificada foi excedida!"},
                    status=400)
        else:
            return Response(
                data={'detail': "A placa mãe não tem suporte ao Processador especificado!"},
                status=400)

    def list(self, request, *args, **kwargs):
        orders = self.queryset.filter()
        serializer_class = OrderSerializer(orders, many=True)
        return Response(serializer_class.data)
