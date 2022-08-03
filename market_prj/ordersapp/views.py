from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.detail import DetailView

from authapp.models import TravelUser
from basketapp.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem
from mainapp.utils import send_email_message
from django.contrib.auth import get_user_model

# from django.db.models.signals import pre_save
# from django.db.models.signals import pre_delete
# from django.dispatch import receiver


# from django.forms import formset_factory




# список заказов
class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# создание заказа с товарными позициями
class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy("ordersapp:orders_list")

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1, fields=['accommodation', 'date_from', 'date_to']
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order,
                    OrderItem,
                    form=OrderItemForm,
                    extra=len(basket_items),
                    fields=['accommodation', 'date_from', 'date_to'],
                )
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial["accommodation"] = basket_items[num].accommodation
                    form.initial["nights"] = basket_items[num].nights
                    form.initial["date_from"] = basket_items[num].date_from
                    form.initial["date_to"] = basket_items[num].date_to
                    form.initial["price"] = basket_items[num].accommodation.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data["orderitems"] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()


        current_order = Order.objects.get(id=self.object.id)
        user = get_user_model().objects.get(pk=self.request.user.pk)
        params = {'nights': current_order.get_total_nights(),
                  'price': current_order.get_total_cost(),
                  'num_order': current_order.id,


                  }
        send_email_message('Успешное бронирование отеля', params, user.email)

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


# редактирование заказа с товарными позициями
class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy("ordersapp:orders_list")

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=1, fields="__all__"
        )
        if self.request.POST:
            data["orderitems"] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data["orderitems"] = OrderFormSet(instance=self.object)
            # formset = OrderFormSet(instance=self.object)
            # for form in formset.forms:
            # if form.instance.pk:
            # form.initial['price'] = form.instance.accommodation.price
            # data['orderitems'] = formset

        return data


# карточка заказа
class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context["title"] = "заказ/просмотр"
        return context


# удаление заказа
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse("ordersapp:orders_list"))
