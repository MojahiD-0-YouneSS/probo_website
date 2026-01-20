from django.urls import path,include
from apps.core import views

app_name='core'
urlpatterns = [
    path('',views.home,name='home'),
    path('menu/',views.menu,name='menu'),
    path('reservation/',views.reservation,name='reservation'),
    path('add/menu/item/',views.add_menu_item,name='add_menu_item'),
    path('add/order/item/',views.add_order_item,name='add_order_item'),
    path('add/order/',views.place_order,name='place_order'),
    path('table/book/',views.book_table,name='book_table'),
    path('process/order/<obj_id>',views.process_order,name='process_order'),
    path('remove/order/item/<obj_id>',views.remove_order_item,name='remove_order_item'),
    path('remove/menu/item/<obj_id>',views.remove_menu_item,name='remove_menu_item'),
]