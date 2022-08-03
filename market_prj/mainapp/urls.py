from django.urls import include, path

import mainapp.views as mainapp

app_name = "mainapp"

urlpatterns = [
    path("", mainapp.AccommodationListView.as_view(), name="index"),
    path("auth/", include("authapp.urls", namespace="auth")),
    path(
        "accommodation_details/<int:pk>/", mainapp.accommodation, name="accommodation"
    ),
]
