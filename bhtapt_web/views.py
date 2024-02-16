from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum,Min,Max
from django.urls import reverse,reverse_lazy
from django.views import View
from .forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from .  models import Payment,Transaction,Account,Cash_Payment
from decimal import Decimal
from datetime import timedelta, datetime
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib.auth.hashers import make_password
from . utils import user_is_superuser
from django.contrib.auth.decorators import user_passes_test
# from weasyprint import HTML


def update_account(instance,payment=None):
    if payment =='cashpayment':
        transactions = Transaction.objects.filter(cash_payment=instance) 
    elif payment =='journal':
        transactions = Transaction.objects.filter(journal=instance)     
    else:    
        transactions = Transaction.objects.filter(payment=instance) 
    for transaction in transactions:
        account =Account.objects.get(id=transaction.account.id)
        total_credits = Transaction.objects.filter(account=account, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_debits = Transaction.objects.filter(account=account, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        account.balance =  total_debits - total_credits
        account.save()

def update_accountbalance(instance,payment=None):
        total_credits = Transaction.objects.filter(account=instance, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_debits = Transaction.objects.filter(account=instance, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        instance.balance =  total_debits - total_credits
        print(instance.balance)
        instance.save()        

# Create your views here.
        
@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'bhtapt_web/index.html')
    
#----------------------------------------------------------------------

#------------------------------Floor Views ----------------------------
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class addfloor(View):
    def get(self, request):
        form = FloorForm()
        action = 'Add Floor'
        return render(request, 'bhtapt_web/addfloor.html',{'form':form,'action':action})
    
    def post(self,request):
        form = FloorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appartment:list_floors')
        else:
            return render(request, 'bhtapt_web/addfloor.html',{'form':form,'action':'Add floor'}) 
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class list_floors(View):
    def get(self, request):
        floors_list = Floor.objects.filter(soft_delete=False)  
        paginator = Paginator(floors_list, 10) 
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, 'bhtapt_web/floorlist.html', {'page_obj': page_obj})      

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class FloorEdit(View):
    template_name = 'bhtapt_web/addfloor.html'
    success_url = 'appartment:list_floors'  # Replace with the name of the URL to redirect after a successful save

    def get(self, request, floor_id=None):
        if floor_id:
            floor_instance = get_object_or_404(Floor, id=floor_id)
            form = FloorForm(instance=floor_instance)
            action = 'Update'
        else:
            return (reverse(self.success_url))
        return render(request, self.template_name, {'form': form,'action':action})

    def post(self, request, floor_id=None):
        if floor_id:
            floor_instance = get_object_or_404(Floor, id=floor_id)
            form = FloorForm(request.POST, instance=floor_instance)
        else:
            form = FloorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(self.success_url))  # Redirect to the success URL
        return render(request, self.template_name, {'form': form,'action':'Update'})           

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class FloorDeleteView(View):
    def get(self, request, floor_id):
        floor = get_object_or_404(Floor, id=floor_id)
        floor.delete()
        return redirect(reverse_lazy('appartment:list_floors'))
    
#--------------------------------------------------------------------------

#------------------------------Category Views ------------------------------
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class CategoryCreateUpdateView(View):
    form_class = CategoryForm
    template_name = 'bhtapt_web/category_form.html'
    success_url = reverse_lazy('appartment:list_category')

    def get(self,request,category_id=None):
        category = get_object_or_404(Category, id=category_id) if category_id else None
        form = self.form_class(instance=category)
        action = 'Add Category' if category_id is None else 'Update Category'
        return render(request, self.template_name, {"form": form,'action':action})
    
    def post(self,request,category_id=None):
        category = get_object_or_404(Category, id=category_id) if category_id else None
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            action = 'Add Category' if category_id is None else 'Update Category'
            return render(request, self.template_name, {"form": form,'action':action})
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class CategoryDeleteView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect(reverse_lazy('appartment:list_category'))

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class list_category(View):
    def get(self, request):
        category_list = Category.objects.filter(soft_delete=False).order_by('-id') 
        paginator = Paginator(category_list, 10) 
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, 'bhtapt_web/categorylist.html', {'page_obj': page_obj})  

#---------------------------------------------------------------------------
    
#------------------------------Room Views ----------------------------------
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class RoomCreateUpdateView(View):
    form_class = RoomForm
    template_name = 'bhtapt_web/roomform.html'
    success_url = reverse_lazy('appartment:list_rooms')

    def get(self,request,room_id=None):
        room = get_object_or_404(Room, id=room_id) if room_id else None
        form = self.form_class(instance=room)
        action = 'Add Room' if room_id is None else 'Update Room'
        return render(request, self.template_name, {"form": form,'action':action})

    def post(self,request,room_id=None):
        room = get_object_or_404(Room, id=room_id) if room_id else None
        form = self.form_class(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            action = 'Add Room' if room_id is None else 'Update Room'
            return render(request, self.template_name, {"form": form,'action':action})

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class RoomDeleteView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return redirect(reverse_lazy('appartment:list_rooms'))        
    
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class list_rooms(View):
    def get(self, request):
        category_room_counts = Room.objects.values('category__category_name').annotate(
            total_rooms=Count('id'),
            vacant_rooms=Count('id', filter=Q(room_status='1')),
            occupied_rooms=Count('id', filter=Q(room_status='2'))
            ).order_by('category__category_name')
        room_list = Room.objects.all().order_by('-id') 
        paginator = Paginator(room_list, 10) 
        total_room_count = Room.objects.count()
        vacant_room_count = Room.objects.filter(room_status='1').count()
        occupied_room_count = Room.objects.filter(room_status='2').count()
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        context = {
            'page_obj': page_obj,
            'categorization': category_room_counts,
            'total_room_count': total_room_count,
            'vacant_room_count': vacant_room_count,
            'occupied_room_count': occupied_room_count
        }
        return render(request, 'bhtapt_web/roomlist.html', context)  


#---------------------------------------------------------------------------
    
#------------------------------Checkin Cehckout / Dashboard Views ----------------------------------    
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        floors = Floor.objects.prefetch_related('room_set').all().order_by('floor_no')
        return render(request, 'bhtapt_web/dashboard.html',{'floors':floors}) 

@method_decorator(login_required, name='dispatch')
class cleaning(View):
    def get(self, request,room_id):
        room =Room.objects.get(id=room_id)
        if room.room_status=='4':
            booking_data = Booking.objects.filter(room=room,status='2')
            if booking_data.exists():
                room.room_status='2'
            else:
                room.room_status='1'
            room.save()
        else:
            room.room_status='4'
            room.save()    
        return redirect('appartment:dashboard')

@method_decorator(login_required, name='dispatch')
class BookingView(View):
    form_class = BookingForm
    template_name = 'bhtapt_web/booking.html'
    success_url = reverse_lazy('appartment:bookingslist')
    def get(self, request,room_id):
        room = Room.objects.get(id=room_id)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            booking_type = request.GET.get('type',None)
            room_rate = room.daily_amount if booking_type == '1' else room.yearly_amount if booking_type=='2' else room.monthly_amount
            return JsonResponse({'room_rate':room_rate}) 
        form = self.form_class
        action='Confirm Check IN'
        return render(request, self.template_name,{'room':room_id,'form':form,'action':action})   
    def post(self,request,room_id):
        if not Booking.objects.filter(room_id=room_id,status ='2').exists():
            form = self.form_class(request.POST)
            if form.is_valid():
                instance=form.save()
                payments = Payment.objects.filter(booking=instance)
                if not payments.exists():
                    return redirect('appartment:booking_reciept', booking_id=instance.id) 
                return redirect('appartment:reciept_print', payment_id=payments.first().id) 
            else:
                action = 'Confirm Check IN' 
                return render(request, self.template_name, {'room':room_id,"form": form,'action':action})
        else:    
            return redirect('appartment:dashboard')    

@method_decorator(login_required, name='dispatch')
class advance_payment(View):
    template_name = 'bhtapt_web/advance_payment.html'
    success_url = reverse_lazy('appartment:dashboard')
    def get(self, request,room_id):
        booking = Booking.objects.filter(room_id=room_id,status='2').last()
        outstanding = booking.calculate_outstanding_amount() or 0.000
        totals_Advance = Payment.objects.filter(booking=booking).aggregate(total=Sum('amount'))['total'] or 0
        # floors = Floor.objects.prefetch_related('room_set').all().order_by('floor_no')
        
        return render(request, self.template_name,{'booking':booking,'advance':totals_Advance,'outstanding':outstanding})     

    def post(self,request,room_id):
        advance_amount = request.POST.get('additional_amount',None)
        booking = Booking.objects.filter(room_id=room_id,status='2').last()
        if advance_payment is not None:
            payment = Payment.objects.create(
                booking=booking,
                amount=advance_amount, 
                payment_status='1',  #  '1' represents a status paid
                narration='Additional Payment',
                payment_date = date.today(),
                from_account = Account.get_advanceAccount(),
                to_account = Account.get_cash_account(),
                room = booking.room  if booking.room else None
            )
            booking.amount_due -= Decimal(advance_amount)
            booking.save()
        return redirect('appartment:reciept_print', payment_id=payment.id)         
    
@method_decorator(login_required, name='dispatch')
class checkoutView(View):
    template_name = 'bhtapt_web/checkout.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request,room_id):
        booking = Booking.objects.filter(room_id=room_id,status='2').last()
        total_amount = Payment.objects.filter(booking=booking).aggregate(total=Sum('amount'))['total']
        print(total_amount)
        if total_amount is None:
            total_amount = 0
        # floors = Floor.objects.prefetch_related('room_set').all().order_by('floor_no')
        bill_no = Payment.objects.count() + 1
        return render(request, self.template_name,{'booking':booking,'advance':round(total_amount,3),'bill_no':bill_no}) 

    def post(self,request,room_id):
        instance = Booking.objects.filter(room_id=room_id,status='2').last()
        total_amount = Payment.objects.filter(booking=instance).aggregate(total=Sum('amount'))['total']
        bill_no = Payment.objects.count() + 1
        checkout_amount= request.POST.get('checkout_anount',None)
        print(checkout_amount)
        if checkout_amount :
                instance.check_out_date = request.POST.get('check_out_date')
                instance.discount = request.POST.get('discount')
                instance.rate = request.POST.get('rate')
                instance.total_amount = request.POST.get('total_amount')
                instance.duration = request.POST.get('duration')
                instance.amount_due=0
                instance.status = "3"
                instance.save()
                instance.room.room_status='4'
                instance.room.save()
                payment = Payment.objects.create(
                booking=instance,
                amount=checkout_amount,
                payment_status='1',  #  '1' represents a status paid
                narration='Checkout Amount',
                from_account = Account.get_checkoutaccount(),
                to_account = Account.get_cash_account(),
                payment_date = date.today())
                return redirect('appartment:reciept_print', payment_id=payment.id)
        else:
             return render(request, self.template_name,{'booking':instance,'advance':round(total_amount,2),'bill_no':bill_no})  
   

 #---------------------------------------------------------------------------
    
#------------------------------Booking List / Booking Reciept ----------------------------------           

@method_decorator(login_required, name='dispatch')
class bookingsList(View):
    template_name = 'bhtapt_web/booking_list.html'
    def get(self, request):
        room_id = request.GET.get('room_id',None)
        if room_id:
            booking_list = Booking.objects.filter(room_id=room_id,soft_delete=False).order_by('-id') 
        else:    
            booking_list = Booking.objects.filter(soft_delete=False).order_by('-id') 
        paginator = Paginator(booking_list, 10) 
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, self.template_name, {'page_obj': page_obj})          

@method_decorator(login_required, name='dispatch')
class bookingdetail(View):
    template_name = 'bhtapt_web/booking_details.html'
    def get(self, request,booking_id):
        booking_list = Booking.objects.get(id=booking_id,soft_delete=False)
        payments= Payment.objects.filter(booking=booking_list)
        return render(request, self.template_name, {'booking': booking_list,'payments':payments})          

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class BookingEdit(View):
    form_class = BookingForm
    template_name = 'bhtapt_web/booking.html'
    success_url = reverse_lazy('appartment:bookingslist')
    def get(self, request,booking_id):
        booking= Booking.objects.get(id=booking_id)
        room = Room.objects.get(id=booking.room.id)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            booking_type = request.GET.get('type',None)
            room_rate = room.daily_amount if booking_type == '1' else room.yearly_amount if booking_type=='2' else room.monthly_amount
            return JsonResponse({'room_rate':room_rate}) 
        form = BookingForm(instance=booking)
        action='Edit Check IN'
        return render(request, self.template_name,{'room':room.id,'form':form,'action':action})   
    def post(self,request,booking_id):
        booking= Booking.objects.get(id=booking_id)
        room = Room.objects.get(id=booking.room.id)
        form = self.form_class(request.POST,instance=booking)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            action = 'Confirm Check IN' 
            return render(request, self.template_name, {'room':room.id,"form": form,'action':action})    

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class BookingDeleteView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        if booking.status == '2' and not Booking.objects.filter(room=booking.room, status ='2').exclude(id=booking_id).exists():
            booking.room.room_status='1'
            booking.room.save()
        transactions = Transaction.objects.filter(booking=booking) 
        for transaction in transactions:
            account =Account.objects.get(id=transaction.account.id)
            total_credits = Transaction.objects.filter(account=account, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
            total_debits = Transaction.objects.filter(account=account, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
            account.balance =  total_debits - total_credits
            account.save()
        booking.delete()
        
        return redirect(reverse_lazy('appartment:bookingslist'))    

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class RecieptEdit(View):
    form_class = BookingForm
    template_name = 'bhtapt_web/edit_payment.html'
    success_url = reverse_lazy('appartment:dashboard')
    def get(self, request,payment_id):
        reciept= Payment.objects.get(id=payment_id)
        action=reciept.narration
        return render(request, self.template_name,{'reciept':reciept,'action':action})    

    def post(self, request,payment_id):
        reciept= Payment.objects.get(id=payment_id)
        amount = request.POST.get('additional_amount',None)
        if amount and Decimal(amount)>0:
            reciept.amount = Decimal(amount) 
            reciept.save(update_fields=['amount'])
            try:
                 transaction = Transaction.objects.get(payment=reciept) 
                 transaction.amount=Decimal(amount)
                 transaction.save()

            except Transaction.DoesNotExist:
                transaction = Transaction.objects.create(payment=reciept,amount=amount,booking=reciept.booking,
                                                         transaction_remark=reciept.narration,transaction_type='debit',account=Account.objects.get_or_create(name="Cash Account", account_type="cash")[0],
                                                         date=reciept.payment_date
                                                        )
            update_account(reciept)
            return redirect(self.success_url)
        else:
            action=reciept.narration   
            return render(request, self.template_name,{'reciept':reciept,'action':action})    
@method_decorator(login_required, name='dispatch')  
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')      
class RecieptDeleteView(View):
    def get(self, request, payment_id):
        reciept = get_object_or_404(Payment, id=payment_id) 
        toaccount = reciept.to_account
        from_account = reciept.from_account
        reciept.delete()
        if toaccount: 
            update_accountbalance(toaccount) 
        if from_account :
            update_accountbalance(from_account)

        return redirect(reverse_lazy('appartment:cashreciept_list'))  

@method_decorator(login_required, name='dispatch')  
class reciept_print(View):
    template_name = 'bhtapt_web/payment_reciept.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request,booking_id=None,payment_id=None):
        if payment_id is not None:
            payment =Payment.objects.get(id=payment_id)
        if booking_id is not None:
            booking=Booking.objects.get(id=booking_id)
            total_advance = Payment.objects.filter(booking=booking,narration__in=['Advance Payment','Additional Payment']).aggregate(total=Sum('amount'))['total']
            total_amountpaid = Payment.objects.filter(booking=booking).aggregate(total=Sum('amount'))['total'] 
            if total_amountpaid is None:
                total_amountpaid=0
            if total_advance is None:
                total_advance=0
            return render(request, 'bhtapt_web/guestreciept.html',{'booking':booking,'amount_paid':total_amountpaid,'advance':total_advance})     
        total_advance = Payment.objects.filter(booking=payment.booking,narration__in=['Advance Payment','Additional Payment']).aggregate(total=Sum('amount'))['total']
        if total_advance is None:
            total_advance=0
        return render(request, self.template_name,{'payment':payment,'advance':total_advance}) 

@method_decorator(login_required, name='dispatch')  
class recieptcashpayment(View):
    template_name = 'bhtapt_web/paymentreciept.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request,payment_id=None,journal_id=None,cash_reciept=None):
        if payment_id is not None:
            payment =Cash_Payment.objects.get(id=payment_id)
            action = 'Cash Payment'
            # return render(request, self.template_name,{'payment':payment}) 
        if journal_id is not None:
            payment =Journel.objects.get(id=journal_id)
            action = 'Journal'
        
        if cash_reciept is not None:
            payment =Payment.objects.get(id=cash_reciept)
            action = 'Cash Reciept'
            # return render(request, self.template_name,{'payment':payment})           
        return render(request, self.template_name,{'payment':payment,'action':action})   

#---------------------------------------------------------------------------
    
#------------------------------Cash Book / Room Details ----------------------------------  
@method_decorator(login_required, name='dispatch')
class CashBookView(View):
    template_name = 'bhtapt_web/cash_book.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request):
           # Get the date from the request or default to today
        filter='daily'
        daily_balances=''
        date_str = request.GET.get('date',None)
        start_date = request.GET.get('start',None)
        end_date = request.GET.get('end', None)
        if date_str:
            current_date = datetime.strptime(date_str, '%b. %d, %Y').date()
        else :
            current_date=date.today()
        cash_account = Account.get_cash_account()
        # Calculate opening and closing balances
        opening_balance = Transaction.get_opening_balance_for_date(current_date,cash_account)
        closing_balance = Transaction.get_closing_balance_until_date(current_date,cash_account)

        # Fetch transactions for the current date

        if 'all' in request.GET:
            transactions = Transaction.objects.filter(account=cash_account).order_by('date')
            filter='all'
            earliest_transaction = Transaction.objects.filter(account=cash_account).earliest('date').date
            latest_transaction = Transaction.objects.filter(account=cash_account).latest('date').date
            date_range = [earliest_transaction + timedelta(days=x) for x in range((latest_transaction - earliest_transaction).days + 1)]
            daily_balances = {day: {'opening': Transaction.get_opening_balance_for_date(day,cash_account),
                        'closing': Transaction.get_closing_balance_until_date(day,cash_account)}
                  for day in date_range}
        elif start_date is not None and end_date is not None:   
            filter = 'range'
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
            daily_balances = {day: {'opening': Transaction.get_opening_balance_for_date(day,cash_account),
                        'closing': Transaction.get_closing_balance_until_date(day,cash_account)}
                  for day in date_range}
            transactions = Transaction.objects.filter(date__range=[start_date, end_date],account=cash_account).order_by('date')
        else:
            transactions = Transaction.objects.filter(date=current_date,account=cash_account).order_by('date')

        # Determine the previous and next dates for pagination
        previous_date = current_date - timedelta(days=1)
        next_date = current_date + timedelta(days=1)

        context = {
            'opening_balance': opening_balance,
            'closing_balance': closing_balance,
            'transactions': transactions,
            'current_date': current_date,
            'previous_date': previous_date,
            'next_date': next_date,
            'filter':filter,
            'daily_balances': daily_balances
        }

        return render(request, self.template_name, context)   

@method_decorator(login_required, name='dispatch')
class CashRecieptListView(View):
    template_name = 'bhtapt_web/cash_reciept.html'
    def get(self, request):
        room_id = request.GET.get('room_id',None)
        if room_id:
            reciepts = Payment.objects.filter(booking__room_id=room_id).order_by('-id')
        else:
            reciepts = Payment.objects.all().order_by('-id')
        paginator = Paginator(reciepts, 10) 
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, self.template_name, {'page_obj': page_obj}) 
    
@method_decorator(login_required, name='dispatch')
class RoomDetails(View):
    template_name = 'bhtapt_web/room_details.html'
    def get(self, request,room_id):
        room_data = Room.objects.get(id=room_id)
        return render(request, self.template_name, {'room': room_data})     
    
#---------------------------------------------------------------------------
    
#------------------------------Login / Log Out ----------------------------------  

class UserLogin(View):
    template_name = 'bhtapt_web/signin.html'
    def get(self, request):
        if request.user.is_authenticated: return redirect('appartment:dashboard')
        return render(request, self.template_name)  
    
    def post(self, request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                return redirect('appartment:dashboard') 
        else:   
                msg='Wrong Username or password'
        return render(request, self.template_name,{'msg':msg})  

class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('appartment:login')
    
#---------------------------------------------------------------------------
    
#------------------------------Accounts / Cash Reciept Add ----------------------------------  

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')      
class AccountAdd_View(View):
    form_class = AccountForm
    template_name = 'bhtapt_web/account_form.html'
    success_url = reverse_lazy('appartment:accounts_list')
    def get(self,request,account_id=None):
        account = get_object_or_404(Account, id=account_id) if account_id else None
        form = self.form_class(instance=account)
        action = 'Add Account' if account_id is None else 'Update Account'
        return render(request, self.template_name, {"form": form,'action':action})
    
    def post(self,request,account_id=None):
        account = get_object_or_404(Account, id=account_id) if account_id else None
        form = self.form_class(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            action = 'Add Account' if account_id is None else 'Update Account'
            return render(request, self.template_name, {"form": form,'action':action})

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')      
class list_accounts(View):
    def get(self, request):
        accounts_list = Account.objects.all().order_by('-id')
        paginator = Paginator(accounts_list, 10) 
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, 'bhtapt_web/accounts_list.html', {'page_obj': page_obj}) 


@method_decorator(login_required, name='dispatch') 
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')      
class AccountDeleteView(View):
    def get(self, request, account_id):
        account = get_object_or_404(Account, id=account_id) 
        # update_account(account)
        account.delete()
        return redirect(reverse_lazy('appartment:accounts_list'))  
    
@method_decorator(login_required, name='dispatch')
class CashRecieptAdd(View):
    form_class = CashReciept_form
    template_name = 'bhtapt_web/cash_recieptform.html'
    success_url = reverse_lazy('appartment:cashreciept_list')
    def get(self,request,payment_id=None):
        if payment_id :
            if not request.user.is_superuser:
                return redirect(self.success_url)
        cashreciept = get_object_or_404(Payment, id=payment_id) if payment_id else None
        form = self.form_class(instance=cashreciept)
        action = 'Add Cash Reciept' if payment_id is None else 'Update Reciept'
        return render(request, self.template_name, {"form": form,'action':action})
    
    def post(self,request,payment_id=None):
        payment = get_object_or_404(Payment, id=payment_id) if payment_id else None
        form = self.form_class(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            action = 'Add Cash Reciept' if payment_id is None else 'Update Reciept'
            return render(request, self.template_name, {"form": form,'action':action})    
        
#---------------------------------------------------------------------------
    
#------------------------------ Cash Payment ----------------------------------     
@method_decorator(login_required, name='dispatch')
class CashPaymentAdd(View):
    form_class = CashPayment_form
    template_name = 'bhtapt_web/cashpayment_form.html'
    success_url = reverse_lazy('appartment:cash_payments')
    def get(self,request,payment_id=None):
        if payment_id :
            if not request.user.is_superuser:
                return redirect(self.success_url)
        cashpayment = get_object_or_404(Cash_Payment, id=payment_id) if payment_id else None
        form = self.form_class(instance=cashpayment)
        action = 'Add Cash Payment' if payment_id is None else 'Update Payment'
        return render(request, self.template_name, {"form": form,'action':action})
    
    def post(self,request,payment_id=None):
        cashpayment = get_object_or_404(Cash_Payment, id=payment_id) if payment_id else None
        form = self.form_class(request.POST, instance=cashpayment)
        room_number = request.POST.get('room_number',None)
        if form.is_valid():
            instance = form.save()
            if room_number is not None:
                try:
                    room_instance = Room.objects.get(room_number=room_number)
                    instance.room=room_instance
                    instance.save()
                except Room.DoesNotExist:
                    pass   
            return redirect(self.success_url)
        else:
            action = 'Add Payment' if payment_id is None else 'Update Payment'
            return render(request, self.template_name, {"form": form,'action':action})          


@method_decorator(login_required, name='dispatch')
class CashPaymentListView(View):
    template_name = 'bhtapt_web/cash_payments.html'
    def get(self, request):
        room_id = request.GET.get('room_id',None)
        if room_id:
            payments = Cash_Payment.objects.filter(room_id=room_id).order_by('-id')
        else:
            payments = Cash_Payment.objects.all().order_by('-id')
        paginator = Paginator(payments, 10)
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, self.template_name, {'page_obj': page_obj}) 


@method_decorator(login_required, name='dispatch')  
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')      
class CashPayment_Delete(View):
    def get(self, request, payment_id):
        payment = get_object_or_404(Cash_Payment, id=payment_id) 
        # update_account(payment,'cashpayment')
        toaccount = payment.to_account
        from_account = payment.from_account
        payment.delete()
        if toaccount: 
            update_accountbalance(toaccount) 
        if from_account :
            update_accountbalance(from_account)
        return redirect(reverse_lazy('appartment:cash_payments'))          
    

#---------------------------------------------------------------------------
    
#------------------------------ Journal ----------------------------------       
    
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class JournalAdd(View):
    form_class = journal_form
    template_name = 'bhtapt_web/journelcreateform.html'
    success_url = reverse_lazy('appartment:journals')
    def get(self,request,payment_id=None):
        journal = get_object_or_404(Journel, id=payment_id) if payment_id else None
        form = self.form_class(instance=journal)
        action = 'Add Journal' if payment_id is None else 'Update Journal'
        return render(request, self.template_name, {"form": form,'action':action})
    
    def post(self,request,payment_id=None):
        journal = get_object_or_404(Journel, id=payment_id) if payment_id else None
        form = self.form_class(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            action = 'Add Journal' if payment_id is None else 'Update Journal'
            return render(request, self.template_name, {"form": form,'action':action})          

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class JournalListView(View):
    template_name = 'bhtapt_web/journals.html'
    def get(self, request):
        room_id = request.GET.get('room_id',None)
        if room_id:
            journals = Journel.objects.filter(room_id=room_id).order_by('-id')
        else:
            journals = Journel.objects.all().order_by('-id')
        paginator = Paginator(journals, 10)
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, self.template_name, {'page_obj': page_obj}) 
    
@method_decorator(login_required, name='dispatch')  
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class Journal_Delete(View):
    def get(self, request, payment_id):
        journal = get_object_or_404(Journel, id=payment_id) 
        toaccount = journal.to_account
        from_account = journal.from_account
        journal.delete()
        if toaccount: 
            update_accountbalance(toaccount) 
        if from_account :
            update_accountbalance(from_account)
        return redirect(reverse_lazy('appartment:journals'))    


#---------------------------------------------------------------------------
    
#------------------------------ Ledger ---------------------------------- 

# @method_decorator(login_required, name='dispatch')
# class LedgerView(View):
#     template_name = 'bhtapt_web/ledger.html'
#     success_url = reverse_lazy('appartment:list_rooms')
#     def get(self, request):
#         accounts = Account.objects.all().order_by('-id')
#            # Get the date from the request or default to today
#         account_id = request.GET.get('account',None)
#         if account_id:
#             filter='daily'
#             daily_balances=''
#             date_str = request.GET.get('date',None)
#             start_date = request.GET.get('start',None)
#             end_date = request.GET.get('end', None)
#             if date_str:
#                 current_date = datetime.strptime(date_str, '%b. %d, %Y').date()
#             else :
#                 current_date=date.today()
#             account = Account.objects.get(id=account_id)
#             # Calculate opening and closing balances
#             opening_balance = Transaction.get_opening_balance_for_date(current_date,account)
#             closing_balance = Transaction.get_closing_balance_until_date(current_date,account)

#             # Fetch transactions for the current date

#             if 'all' in request.GET:
#                 transactions = Transaction.objects.filter(account=account).order_by('date')
#                 filter='all'
#                 earliest_transaction = Transaction.objects.filter(account=account).earliest('date').date
#                 latest_transaction = Transaction.objects.filter(account=account).latest('date').date
#                 date_range = [earliest_transaction + timedelta(days=x) for x in range((latest_transaction - earliest_transaction).days + 1)]
#                 daily_balances = {day: {'opening': Transaction.get_opening_balance_for_date(day,account),
#                             'closing': Transaction.get_closing_balance_until_date(day,account)}
#                     for day in date_range}
#             elif start_date is not None and end_date is not None:   
#                 filter = 'range'
#                 start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#                 end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
#                 date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
#                 daily_balances = {day: {'opening': Transaction.get_opening_balance_for_date(day,account),
#                             'closing': Transaction.get_closing_balance_until_date(day,account)}
#                     for day in date_range}
#                 transactions = Transaction.objects.filter(date__range=[start_date, end_date],account=account).order_by('date')
#             else:
#                 transactions = Transaction.objects.filter(date=current_date,account=account).order_by('date')

#             # Determine the previous and next dates for pagination
#             previous_date = current_date - timedelta(days=1)
#             next_date = current_date + timedelta(days=1)

#             context = {
#                 'opening_balance': opening_balance,
#                 'closing_balance': closing_balance,
#                 'transactions': transactions,
#                 'current_date': current_date,
#                 'previous_date': previous_date,
#                 'next_date': next_date,
#                 'filter':filter,
#                 'daily_balances': daily_balances,
#                 'accounts': accounts,
#                 'account': account,
#             }
#             return render(request, self.template_name, context) 
#         else:
#             context = {
#                 'accounts': accounts
#             }
#             return render(request, self.template_name, context) 

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class account_ledger_view(View):
    template_name = 'bhtapt_web/ledger.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request):
        accounts = Account.objects.all().order_by('-id')
        date_str = request.GET.get('date',None)
        start_date = request.GET.get('start',None)
        starting_balance=0
        opening_balance =0
        filter=False

        end_date = request.GET.get('end', None)
        # Assuming 'account_id' is passed to this view to identify the account
        account_id = request.GET.get('account',None)
        if account_id:
            account = Account.objects.get(id=account_id)
            if start_date and end_date:
                try:
                    starting_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    filter=True
                    ending_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    # Calculate the opening balance for the start date
                    previous_day = starting_date - timedelta(days=1)
                    starting_balance = Transaction.get_closing_balance_until_date(previous_day, account)
                    opening_balance = starting_balance

                    transactions = Transaction.objects.filter(account=account, date__gte=starting_date, date__lte=ending_date).order_by('date')
                except ValueError:
                    # Handle invalid date format
                    starting_date = 'invalid_date'
                    ending_date = 'invalid date'
                    transactions = Transaction.objects.filter(account=account).order_by('date')
            else:
                transactions = Transaction.objects.filter(account=account).order_by('date')
                date_range = Transaction.objects.filter(account=account).aggregate(start_date=Min('date'), end_date=Max('date'))
                starting_date = date_range.get('start_date')
                ending_date = date_range.get('end_date')
            ledger_data = []
            running_balance = starting_balance
            total_credits = 0
            total_debits = 0

            for transaction in transactions:
                # Determine the type of transaction
                if transaction.journal:
                    trans_type = 'Journal'
                elif transaction.cash_payment:
                    trans_type = 'Cash Payment'
                elif transaction.payment:
                    trans_type = 'Cash Reciept'
                else:
                    trans_type = 'Other'

                # Update running balance, total credits, and total debits
                if transaction.transaction_type == 'credit':
                    running_balance -= transaction.amount
                    credit = transaction.amount
                    debit = 0
                    total_credits += credit
                else:
                    running_balance += transaction.amount
                    debit = transaction.amount
                    credit = 0
                    total_debits += debit

                # Append transaction data to ledger_data
                ledger_data.append({
                    'date': transaction.date,
                    'transaction_id': transaction.payment.id if transaction.payment else transaction.cash_payment.id if transaction.cash_payment else transaction.journal.id,
                    'type': trans_type,
                    'description': transaction.transaction_remark,
                    'debit': debit,
                    'credit': credit,
                    'balance': running_balance
                })

            context = {
                'accounts': accounts,
                'ledger_data': ledger_data,
                'account': account,
                'total_credits': total_credits + abs(opening_balance) if opening_balance < 0 else total_credits  if opening_balance == 0 else total_credits,
                'total_debits': total_debits + abs(opening_balance) if opening_balance > 0 else total_debits  if opening_balance == 0 else total_debits,
                'ending_balance': running_balance,
                'starting_date':starting_date,
                'positive_openingbalance':abs(opening_balance),
                'ending_date':ending_date,
                'opening_balance': opening_balance or 0,
                'filter' : filter 
            }
        else:
            context = {
                'accounts': accounts,
            }

        return render(request, self.template_name, context)
    
#----------------------------------------------------------------------

#------------------------------Users Views ----------------------------
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class AddUser(View):
    template_name = 'bhtapt_web/adduser.html'
    success_url = 'appartment:list_floors'
    form_class = AddUsersForm

    def get(self, request,user_id=None):
        user = get_object_or_404(User, id=user_id) if user_id else None
        form = self.form_class(instance=user)
        action = 'Add User' if user_id is None else 'Update User'
        return render(request, self.template_name, {"form": form,'action':action})
    
    def post(self,request,user_id=None):
        user = get_object_or_404(User, id=user_id) if user_id else None
        form = AddUsersForm(request.POST,instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            form.save()
            return redirect('appartment:users_list')
        else:
            return render(request, 'bhtapt_web/adduser.html',{'form':form,'action':'Add User'})     


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class UserListView(View):
    template_name = 'bhtapt_web/userslist.html'
    def get(self, request):
        users = User.objects.filter(user_type__in=['2','3']).order_by('-id')
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, self.template_name, {'page_obj': page_obj})          
    
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class UserEdit(View):
    template_name = 'bhtapt_web/adduser.html'
    success_url = 'appartment:users_list' 

    def get(self, request, user_id=None):
        if user_id:
            user_instance = get_object_or_404(User, id=user_id)
            form = AddUsersForm(instance=user_instance)
            action = 'Update'
        else:
            return (reverse(self.success_url))
        return render(request, self.template_name, {'form': form,'action':action})

    def post(self, request, user_id=None):
        if user_id:
            user_instance = get_object_or_404(User, id=user_id)
            form = AddUsersForm(request.POST, instance=user_instance)
        else:
            form = AddUsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(self.success_url))  # Redirect to the success URL
        return render(request, self.template_name, {'form': form,'action':'Update'})       
    

@method_decorator(login_required, name='dispatch')  
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class UserDeleteView(View):
    def get(self, request, user_id):
        account = get_object_or_404(User, id=user_id) 
        # update_account(account)
        account.delete()
        return redirect(reverse_lazy('appartment:users_list'))      
    

@method_decorator(login_required, name='dispatch')  
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class CashFlowView(View):
    template_name = 'bhtapt_web/cashflow.html'
    success_url = 'appartment:users_list' 
    def get(self, request):
        income = Transaction.objects.filter(account=Account.get_cash_account(),transaction_type="debit")
        expense = Transaction.objects.filter(account = Account.get_cash_account(),transaction_type="credit")
        return render(request,self.template_name)    
    

@method_decorator(login_required, name='dispatch')  
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class TotalOutstanding(View):
    template_name = 'bhtapt_web/outstanding.html'
    success_url = 'appartment:users_list' 
    def get(self, request):
        bookings = Booking.objects.filter(status='2').order_by("room__room_number")
        total_outstanding=0
        for booking in bookings:
            total_outstanding += booking.calculate_outstanding_amount()
        return render(request,self.template_name,{'data':bookings,'total':total_outstanding,'date':datetime.today()})    

@method_decorator(login_required, name='dispatch')  
@method_decorator(user_passes_test(user_is_superuser), name='dispatch')
class ReportsView(View):
    template_name = 'bhtapt_web/reports.html'
    success_url = 'appartment:users_list' 
    def get(self, request):
        report_items = [{'value':'checkin','name':'Checkin Report'},{'value':'checkout','name':'Checkout Report'},{'value':'advance','name':'Advance Report'} ,{'value':'outstanding','name':'Outstanding Amount Report'}]
        reporting_value = request.GET.get('report', None)
        start_date = request.GET.get('start',None)
        end_date = request.GET.get('end',None)
        if start_date and end_date:
            starting_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            ending_date = datetime.strptime(end_date, '%Y-%m-%d').date() 
        else:
            starting_date,ending_date = None,None



        if reporting_value == "checkin":
            report = Payment.objects.filter(narration="Advance Payment").order_by('-id')
            opening_balance = self.get_openingbalance(report,starting_date,'Advance Payment')
            clossing_balance = self.get_clossingbalance(report,ending_date,'Advance Payment')
            if start_date  and end_date:
                report = self.date_filter(report,start_date,end_date)
        elif reporting_value == "checkout":
            report = Payment.objects.filter(narration="Checkout Amount").order_by('-id')
            opening_balance = self.get_openingbalance(report,starting_date,'Checkout Amount')
            clossing_balance = self.get_clossingbalance(report,ending_date,'Checkout Amount')
            if start_date  and end_date:
                report = self.date_filter(report,start_date,end_date)
        elif reporting_value == "advance":
            report = Payment.objects.filter(narration="Additional Payment").order_by('-id')
            opening_balance = self.get_openingbalance(report,starting_date,'Additional Payment')
            clossing_balance = self.get_clossingbalance(report,ending_date,'Additional Payment')
            if start_date  and end_date:
                report = self.date_filter(report,start_date,end_date)   
        else:
            report = None         
        date_range = report.aggregate(start_date=Min('payment_date'), end_date=Max('payment_date'),totalamount = Sum('amount')) if report else {}
        context ={'report_items':report_items,
                  'reports':report,
                  'reporting':reporting_value,
                  'starting_date': date_range.get('start_date',None),
                  'ending_date': date_range.get('end_date',None),
                  'total_amount':date_range.get('totalamount',None),
                  'opening_balance':opening_balance if report else 0,
                  'closing_balance':clossing_balance if report else 0,
                  'Report_Name': 'Check In Report' if reporting_value == "checkin" else 'CheckOut Report' if reporting_value == 'checkout' else 'Advance Report'
                  } 
        return render(request,self.template_name,context)     

    def date_filter(self,queryset,start_date,end_date):
        try:
            starting_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            ending_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            report_data = queryset.filter(payment_date__range=(starting_date, ending_date))
            return report_data
        except Exception as e:
            starting_date = 'invalid_date'
            ending_date = 'invalid date'
            print (e)
            return queryset    

    def get_clossingbalance(self, queryset, date=None,type=None):
        # print(queryset)
        if date is None:
            date = Payment.objects.filter(narration = type).last().payment_date or None 
        try:
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d').date()
            closing_balance = queryset.filter(payment_date__lte=date).aggregate(total=Sum('amount'))
            return closing_balance.get('total', 0)
        except Exception as e:
            print(f"Error in get_closingbalance: {e}")
            return 0

    def get_openingbalance(self, queryset, date=None,type=None):
        if date is None:
            date = Payment.objects.filter(narration = type).first().payment_date or None 
        try:
            previous_day = date - timedelta(days=1)
            opening_balance = self.get_clossingbalance(queryset, previous_day,type)
            return opening_balance or 0
        except Exception as e:
            print(f"Error in get_openingbalance: {e}")
            return 0


        
       
        

