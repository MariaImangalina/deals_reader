from django.db import models
from django.db.models import Sum


class CustomerQuerySet(models.QuerySet):
    def most_spending(self):
        return self.annotate_spent_money().order_by("-spent_money")

    def annotate_spent_money(self):
        return self.annotate(spent_money=Sum("orders__total"))


class Customer(models.Model):
    """
    Модель клиента
    """

    objects = CustomerQuerySet.as_manager()
    username = models.CharField("Имя клиента", max_length=50)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.username

    def get_common_items(self):
        common_items = Order.objects.filter(
            customer_id__in=Customer.objects.exclude(id=self.id)
            .most_spending()[:4]
            .values_list("id", flat=True)
        ).values_list("item", flat=True)

        return (
            self.orders.filter(item__in=common_items)
            .values_list("item", flat=True)
            .order_by()
            .distinct()
        )


class Order(models.Model):
    """
    Модель заказа
    """

    customer = models.ForeignKey(
        "deal.Customer", on_delete=models.CASCADE, related_name="orders"
    )
    item = models.CharField("Камень", max_length=50)
    total = models.PositiveIntegerField("Сумма заказа")
    quantity = models.PositiveIntegerField("Количество камней в заказе")
    date = models.DateTimeField("Дата заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.customer.username} - {self.item}"
