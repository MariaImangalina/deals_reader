from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Customer, Order
from .serializers import CustomerSerializer, DealCreateSerializer
from .utils import dispatch_csv_to_db


class CustomerAPIView(APIView):
    """
    API для обработки данных по сделкам
    метод GET возвращает список клиентов с максимальной общей суммой заказов
    метод POST принимает файл со списком клиентов и вносит их в базу данных
    """
    serializer_class = CustomerSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self, queryset=None):
        return Customer.objects.most_spending().prefetch_related("orders")[:5]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DealCreateSerializer
        elif self.request.method == "GET":
            return CustomerSerializer

    @method_decorator(cache_page(60 * 10, key_prefix="deals_list"))
    def get(self, request, *args, **kwargs):
        """
        :returns список клиентов с максимальной общей суммой заказов
        """
        data = {
            "response": self.get_serializer_class()(self.get_queryset(), many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        :param data - csv-файл со списком сделок
        :returns статус загрузки файла
        """
        data_file = self.get_serializer_class()(data=request.data)
        if data_file.is_valid():
            try:
                dispatch_csv_to_db(data_file.validated_data["data"])
                cache.clear()
                message = {"detail": "Your file was successfully uploaded"}
                return Response(message, status=status.HTTP_200_OK)
            except Exception as exc:
                return Response(
                    {"Status": "Error", "Descr": str(exc)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
