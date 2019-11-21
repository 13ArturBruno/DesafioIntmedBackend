from django.db import models


class Brand(models.Model):
    name = models.CharField('Nome', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"


class Processor(models.Model):
    product = models.CharField('Produto', max_length=60)
    brand = models.ForeignKey(Brand,verbose_name="Marca", related_name='marca', on_delete=models.CASCADE)

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "Processador"
        verbose_name_plural = "Processadores"


class RamMemory(models.Model):
    product = models.CharField('Produto', max_length=60)
    size = models.IntegerField('Tamanho')

    def __str__(self):
        return self.product + "  -  " + str(self.size) + "GB"

    class Meta:
        verbose_name = "Memória Ram"
        verbose_name_plural = "Memórias Ram"


class MotherBoard(models.Model):
    product = models.CharField('Produto', max_length=60, unique=True)
    cpuSupport = models.ManyToManyField(Brand, verbose_name="Processadores Suportados", related_name="cpu_support")
    ramSlots = models.IntegerField('Quantidade de Slots de Memória Ram')
    maxMemorySize = models.IntegerField('Capacidade de Memória Ram Suportada')
    videoOnboard = models.BooleanField('Video Integrado')

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "Placa Mãe"
        verbose_name_plural = "Placas Mãe"


class VideoBoard(models.Model):
    product = models.CharField('Usuário', max_length=60, unique=True)

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = "Placa de Video"
        verbose_name_plural = "Placas de Video"
