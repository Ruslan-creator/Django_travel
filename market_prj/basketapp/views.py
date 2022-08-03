from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Accommodation

from market_prj import settings

# отображение списка записей корзины
@login_required
def basket(request):
    title = "корзина"
    basket_items = Basket.objects.filter(user=request.user).order_by(
        "accommodation__country"
    )

    content = {
        "title": title,
        "basket_items": basket_items,
    }

    return render(request, "basketapp/basket.html", content)


# добавление продукта в корзину
def basket_add(request, pk):

    if "login" in request.META.get("HTTP_REFERER"):
        return HttpResponseRedirect(reverse("acc:accommodations", args=[pk]))

    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, f'/list_of_accommodations/accommodation_details/{pk}/'))

    accommodation = get_object_or_404(Accommodation, pk=pk)
    basket = Basket.objects.filter(
        user=request.user, accommodation=accommodation
    ).first()

    if not basket:
        basket = Basket(user=request.user, accommodation=accommodation)

    basket.nights += 1
    basket.save()

    return HttpResponseRedirect(reverse("ordersapp:order_create"))


# удаление продукта из корзины
@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_edit(request, pk, nights):
    print("привет")
    if request.is_ajax():
        nights = int(nights)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if nights > 0:
            new_basket_item.nights = nights
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by(
            "accommodation__country"
        )

        content = {
            "basket_items": basket_items,
        }

        result = render_to_string("basketapp/includes/inc_basket_list.html", content)

        return JsonResponse({"result": result})
