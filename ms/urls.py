from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
urlpatterns=[
    path('ms/<str:user>', views.ms_index, name="ms_index"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)