from django.urls import path
from . import views
from .views import CustomOrder
from .views import addCustomerOrder



urlpatterns = [
    path('', views.index, name="homepage"),
    path("customer-order/add/", addCustomerOrder, name='add-customer-order'),
]