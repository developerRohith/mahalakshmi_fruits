from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import path, include


def home(request):
    return HttpResponse(
        '<h1>Welcome to Mahalakshmi Pazhamuthirsolai 🍎</h1>'
        '<p>Project setup successful.</p>'
    )


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("products.urls")),

    path("accounts/", include("accounts.urls")),

    path("orders/", include("orders.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )