from django.conf.urls import include,url
from .views import sheetView

urlpatterns=[
url(r'^sheetviewurl/?$',sheetView.as_view())
]