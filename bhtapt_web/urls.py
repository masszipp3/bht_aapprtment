from django.urls import path
from .views import *

app_name = 'appartment'

urlpatterns=[
    path('dashbord',IndexView.as_view(),name='home'),

#------------------------------floor urls ----------------------------    

    path('floors/add',addfloor.as_view(),name='addfloor'),
    path('floors',list_floors.as_view(),name='list_floors'),
    path('floors/<int:floor_id>/edit',FloorEdit.as_view(),name='edit_floors'),
    path('floors/<int:floor_id>/delete',FloorDeleteView.as_view(),name='delete_floors'),

#------------------------------Category urls ----------------------------  

    path('category/add',CategoryCreateUpdateView.as_view(),name='add_category'),
    path('category',list_category.as_view(),name='list_category'),
    path('category/<int:category_id>/edit',CategoryCreateUpdateView.as_view(),name='edit_category'),
    path('category/<int:category_id>/delete',CategoryDeleteView.as_view(),name='delete_category'),

#------------------------------Room urls ----------------------------  

    path('rooms/add',RoomCreateUpdateView.as_view(),name='add_room'),
    path('rooms',list_rooms.as_view(),name='list_rooms'),
    path('rooms/<int:room_id>/edit',RoomCreateUpdateView.as_view(),name='edit_room'),
    path('rooms/<int:room_id>/delete',RoomDeleteView.as_view(),name='delete_room'),
    path('rooms/<int:room_id>/details',RoomDetails.as_view(),name='room_Details'),


#------------------------------Dashboard and Booking urls ---------------------------- 
 
    path('',DashboardView.as_view(),name='dashboard'),
    path('booking/<int:room_id>/check_in',BookingView.as_view(),name='booking'),
    path('booking/<int:room_id>/check_out',checkoutView.as_view(),name='checkout'),
    path('booking/<int:room_id>/advance_payment',advance_payment.as_view(),name='advance'),
    path('booking/list',bookingsList.as_view(),name='bookingslist'),
    path('booking/<int:booking_id>/detail',bookingdetail.as_view(),name='bookingdetail'),
    path('booking/<int:booking_id>/edit',BookingEdit.as_view(),name='bookingedit'),
    path('booking/<int:booking_id>/delete',BookingDeleteView.as_view(),name='bookingdelete'),

#------------------------------Reciepts edit, delete Urls ---------------------------- 

    path('reciept/<int:payment_id>/edit',RecieptEdit.as_view(),name='reciept_edit'),
    path('reciept/<int:payment_id>/delete',RecieptDeleteView.as_view(),name='reciept_delete'),
    path('reciept/<int:payment_id>/print',reciept_print.as_view(),name='reciept_print'),

#------------------------------Cash Book / Room Filter ---------------------------- 

    path('cashbook',CashBookView.as_view(),name='cashbook'),
    path('cash_reciepts/list',CashRecieptListView.as_view(),name='cashreciept_list'),

#------------------------------Login / Logout ---------------------------- 

    path('login',UserLogin.as_view(),name='login'),























]