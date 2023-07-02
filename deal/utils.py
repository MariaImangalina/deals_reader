import csv
import io
from datetime import datetime

from .models import Customer, Order


def dispatch_csv_to_db(data_file):
    dict_data = csv.DictReader(io.StringIO(data_file.read().decode("utf-8")))

    # очищаем базу данных перед новой загрузкой
    Customer.objects.all().delete()

    for row in dict_data:
        RawOrder(row).create()


class RawOrder(object):
    """
    Класс для парсинга файла
    """
    def __init__(self, data: dict):
        self.customer_name = data.get("customer", None)
        self.item = data.get("item", None)
        self.total = data.get("total", None)
        self.quantity = data.get("quantity", None)
        self.date = data.get("date", None)

    def create(self):
        assert all(
            [self.item, self.total, self.quantity, self.date, self.customer_name]
        ), "Недостаточно данных для создания записи"

        defaults = dict(
            item=self.item,
            total=self.total,
            quantity=self.quantity,
            date=datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S.%f"),
        )

        customer = Customer.objects.filter(username=self.customer_name)
        if customer.exists():
            customer = customer.first()
        else:
            customer = Customer.objects.create(username=self.customer_name)
        defaults.update(customer=customer)

        Order.objects.create(**defaults)
