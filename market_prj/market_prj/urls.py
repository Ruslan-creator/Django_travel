from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
import mainapp.views as mainapp


urlpatterns = [
    path("", mainapp.main, name="main"),
    path("list_of_accommodations/", include("mainapp.urls", namespace="acc")),
    path("auth/", include("authapp.urls", namespace="auth")),
    path("", include("social_django.urls", namespace="social")),
    path("admin/", include("adminapp.urls", namespace="admin")),
    path("basket/", include("basketapp.urls", namespace="basket")),
    path("order/", include("ordersapp.urls", namespace="order")),
    # path('admins/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


