from django.urls import path
from Tracker.views import *

urlpatterns = [
    path('',index,name="index"),
    path('delete-transaction/<uuid>',delete_transaction,name="delete_transaction")
]