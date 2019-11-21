from rest_framework.routers import DefaultRouter
from api.order import viewsets as order_views

routers = DefaultRouter()

routers.register("order", order_views.OrderViewSet, base_name="order")






