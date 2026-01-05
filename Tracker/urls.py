from django.urls import path
from Tracker.views import *

urlpatterns = [
    path('',index,name="index"),
    path('delete-transaction/<uuid>',delete_transaction,name="delete_transaction"),
    path('add_registration/',registration,name="registration"),
    path('user_login/',login_page,name="login"),
    path('logout/',logout_page, name = "logout"),
]