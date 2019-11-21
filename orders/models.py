from django.db import models

# Create your models here.
from products.models import Processor, RamMemory, MotherBoard, VideoBoard


class Order(models.Model):
    email = models.EmailField("Email do Cliente", max_length=100)
    processor = models.ForeignKey(Processor, verbose_name='Processador', related_name='processor', on_delete=models.CASCADE)
    ramMemory = models.ManyToManyField(RamMemory, verbose_name='Memória Ram', related_name='ram_memory', blank=True)
    motherBoard = models.ForeignKey(MotherBoard, verbose_name='Placa Mãe', related_name='mother_board', on_delete=models.CASCADE)
    videoBoard = models.ForeignKey(VideoBoard, verbose_name='Placa de Video', related_name='video_board', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Pedido de " + self.email

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
