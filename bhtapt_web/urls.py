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
    path('cleaning/<int:room_id>',cleaning.as_view(),name='cleaning'),
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
    path('booking/<int:booking_id>/print',reciept_print.as_view(),name='booking_reciept'),


#------------------------------Cash Book / Room Filter ---------------------------- 

    path('cashbook',CashBookView.as_view(),name='cashbook'),
    path('cash_reciepts/list',CashRecieptListView.as_view(),name='cashreciept_list'),

#------------------------------Login / Logout ---------------------------- 

    path('login',UserLogin.as_view(),name='login'),
    path('logout',UserLogout.as_view(),name='logout'),


#------------------------------Account / Cash Reciepts ----------------------------
 
    path('account/add',AccountAdd_View.as_view(),name='add_account'),
    path('accounts',list_accounts.as_view(),name='accounts_list'),
    path('account/<int:account_id>/edit',AccountAdd_View.as_view(),name='edit_account'),
    path('account/<int:account_id>/delete',AccountDeleteView.as_view(),name='delete_account'),
    path('cash_reciepts/add',CashRecieptAdd.as_view(),name='add_cashreciept'),
    path('cash_reciepts/<int:cash_reciept>/print',recieptcashpayment.as_view(),name='cashreciept_print'),


#------------------------------Cash Payments  ----------------------------

    path('cash_payments/add',CashPaymentAdd.as_view(),name='add_cashpayment'),
    path('cash_payments/list',CashPaymentListView.as_view(),name='cash_payments'),
    path('cash_payments/<int:payment_id>/edit',CashPaymentAdd.as_view(),name='edit_cashpayment'),
    path('cash_payments/<int:payment_id>/delete',CashPayment_Delete.as_view(),name='delete_cashpayment'),
    path('cash_payments/<int:payment_id>/print',recieptcashpayment.as_view(),name='cashpayment_print'),


#------------------------------ Journal  ---------------------------------

    path('journal/add',JournalAdd.as_view(),name='add_journal'),
    path('journal/list',JournalListView.as_view(),name='journals'),
    path('journal/<int:payment_id>/edit',JournalAdd.as_view(),name='edit_journal'),
    path('journal/<int:payment_id>/delete',Journal_Delete.as_view(),name='delete_journal'),
    path('journal/<int:journal_id>/print',recieptcashpayment.as_view(),name='jounalprint'),


#------------------------------ Ledger  ----------------------------

    path('ledger',account_ledger_view.as_view(),name='ledger'),


#------------------------------ User Management  ----------------------------

    path('users/add',AddUser.as_view(),name='add_user'),
    path('users/<int:user_id>/edit',AddUser.as_view(),name='edit_user'),
    path('users/<int:user_id>/delete',UserDeleteView.as_view(),name='delete_user'),
    path('users/list',UserListView.as_view(),name='users_list'),


#------------------------------ Cash Flow  ----------------------------

    path('cashflow',CashFlowView.as_view(),name='cashflow'),


#------------------------------  Oustanding  ----------------------------

    path('outstanding',TotalOutstanding.as_view(),name='outstanding'),

#------------------------------  Reports  ----------------------------

    path('reports',ReportsView.as_view(),name='reports'),


#------------------------------  Customer  ----------------------------

    path('get_customer',GetCustomer.as_view(),name='customer'),    

#------------------------------  Change Room  ----------------------------

    path('changeroom',Change_RoomView.as_view(),name='changeroom'),    
    path('update/customers',UpdateAllBookingCustomers.as_view(),name='update_customers'),
    path('update/payments',UpdatePaymentTransaction.as_view(),name='update_transaction'),



































]