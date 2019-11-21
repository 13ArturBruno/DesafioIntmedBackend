from django.contrib import admin

# Register your models here.
from products.models import Processor, RamMemory, MotherBoard, VideoBoard, Brand


class MotherBoardAdmin(admin.ModelAdmin):
    filter_horizontal = ['cpuSupport',]


admin.site.register(Processor)
admin.site.register(RamMemory)
admin.site.register(MotherBoard, MotherBoardAdmin)
admin.site.register(VideoBoard)
admin.site.register(Brand)