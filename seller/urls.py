from django.urls import path
from . import views

urlpatterns = [
    path('',views.seller_login,name='sellerlogin'),
    path('index/',views.seller_index,name='sellerindex'),
    path('addproduct/',views.seller_addproduct,name='addproduct'),
    path('manageproduct/',views.manageproduct,name='manageproduct'),
    path('edit/<int:pid>',views.edit,name='edit'),
    path('delete/<int:pid>',views.delete,name='delete'),
]