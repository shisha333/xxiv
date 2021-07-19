from django.contrib import admin
from django.urls import path, include
from authentication import views as authView

urlpatterns = [
    path('', authView.index, name='index'),
    path('contact', authView.contact, name='contact'),
    path('register', authView.Register.as_view(), name='register'),
    path('order', authView.CustomOrderCreateView.as_view(), name='order'),
    path('<user>/confirm-email/', authView.confirmEmail, name='confirm-email'),
    # path('populate-locations/', authView.populate_locations, name='login'),
]