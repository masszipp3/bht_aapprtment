from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum
from django.urls import reverse,reverse_lazy
from django.views import View
from .forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from .  models import Payment,Transaction,Account
from decimal import Decimal
from datetime import timedelta, datetime
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def update_account(instance):
    transactions = Transaction.objects.filter(payment=instance) 
    for transaction in transactions:
        account =Account.objects.get(id=transaction.account.id)
        total_credits = Transaction.objects.filter(account=account, transaction_type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
        total_debits = Transaction.objects.filter(account=account, transaction_type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
        account.balance =  total_debits - total_credits
        account.save()

# Create your views here.
        
@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'bhtapt_web/index.html')
    
#----------------------------------------------------------------------

#------------------------------Floor Views ----------------------------
@method_decorator(login_required, name='dispatch')
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
class list_floors(View):
    def get(self, request):
        floors_list = Floor.objects.filter(soft_delete=False)  
        paginator = Paginator(floors_list, 10) 
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, 'bhtapt_web/floorlist.html', {'page_obj': page_obj})      

@method_decorator(login_required, name='dispatch')
class FloorEdit(View,LoginRequiredMixin):
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
class FloorDeleteView(View,LoginRequiredMixin):
    def get(self, request, floor_id):
        floor = get_object_or_404(Floor, id=floor_id)
        floor.delete()
        return redirect(reverse_lazy('appartment:list_floors'))
    
#--------------------------------------------------------------------------

#------------------------------Category Views ------------------------------
@method_decorator(login_required, name='dispatch')
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
class CategoryDeleteView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return redirect(reverse_lazy('appartment:list_category'))

@method_decorator(login_required, name='dispatch')
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
class RoomDeleteView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return redirect(reverse_lazy('appartment:list_rooms'))        
    
@method_decorator(login_required, name='dispatch')
class list_rooms(View):
    def get(self, request):
        room_list = Room.objects.all().order_by('-id') 
        paginator = Paginator(room_list, 10) 
        page_number = request.GET.get('page')  # Get the page number from the query string
        page_obj = paginator.get_page(page_number)  # Get the page object
        return render(request, 'bhtapt_web/roomlist.html', {'page_obj': page_obj})  


#---------------------------------------------------------------------------
    
#------------------------------Checkin Cehckout / Dashboard Views ----------------------------------    
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        floors = Floor.objects.prefetch_related('room_set').all().order_by('floor_no')
        return render(request, 'bhtapt_web/dashboard.html',{'floors':floors}) 
    

@method_decorator(login_required, name='dispatch')
class BookingView(View):
    form_class = BookingForm
    template_name = 'bhtapt_web/booking.html'
    success_url = reverse_lazy('appartment:list_rooms')
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
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            action = 'Confirm Check IN' 
            return render(request, self.template_name, {"form": form,'action':action})

@method_decorator(login_required, name='dispatch')
class advance_payment(View):
    template_name = 'bhtapt_web/advance_payment.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request,room_id):
        booking = Booking.objects.filter(room_id=room_id,status='2').last()
        # floors = Floor.objects.prefetch_related('room_set').all().order_by('floor_no')
        return render(request, self.template_name,{'booking':booking})     

    def post(self,request,room_id):
        advance_amount = request.POST.get('additional_amount',None)
        booking = Booking.objects.filter(room_id=room_id,status='2').last()
        if advance_payment is not None:
            payment = Payment.objects.create(
                booking=booking,
                amount=advance_amount, 
                payment_status='1',  #  '1' represents a status paid
                narration='Additional Payment',
                payment_date = date.today()
            )
            booking.amount_due -= Decimal(advance_amount)
            booking.save()
        return redirect(self.success_url)           
    
@method_decorator(login_required, name='dispatch')
class checkoutView(View):
    template_name = 'bhtapt_web/checkout.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request,room_id):
        booking = Booking.objects.filter(room_id=room_id,status='2').last()
        total_amount = Payment.objects.filter(booking=booking).aggregate(total=Sum('amount'))['total']
        # floors = Floor.objects.prefetch_related('room_set').all().order_by('floor_no')
        bill_no = Payment.objects.count() + 1
        return render(request, self.template_name,{'booking':booking,'advance':round(total_amount,2),'bill_no':bill_no}) 

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
                payment = Payment.objects.create(
                booking=instance,
                amount=checkout_amount, 
                payment_status='1',  #  '1' represents a status paid
                narration='Checkout Amount',
                payment_date = date.today())
                instance.save()
                instance.room.room_status='1'
                instance.room.save()
                return redirect(self.success_url)
        else:
             return render(request, self.template_name,{'booking':instance,'advance':round(total_amount,2),'bill_no':bill_no})  
   
            

 #---------------------------------------------------------------------------
    
#------------------------------Booking List / Booking Reciept ----------------------------------           

@method_decorator(login_required, name='dispatch')
class bookingsList(View):
    template_name = 'bhtapt_web/booking_list.html'
    def get(self, request):
        room_id = request.POST.get('room_id',None)
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
class BookingEdit(View):
    form_class = BookingForm
    template_name = 'bhtapt_web/booking.html'
    success_url = reverse_lazy('appartment:list_rooms')
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
class BookingDeleteView(View):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        if booking.status == '2':
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
class RecieptEdit(View):
    form_class = BookingForm
    template_name = 'bhtapt_web/edit_payment.html'
    success_url = reverse_lazy('appartment:list_rooms')
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
class RecieptDeleteView(View):
    def get(self, request, payment_id):
        reciept = get_object_or_404(Payment, id=payment_id) 
        update_account(reciept)
        reciept.delete()
        return redirect(reverse_lazy('appartment:bookingslist'))  

class reciept_print(View,LoginRequiredMixin):
    template_name = 'bhtapt_web/payment_reciept.html'
    success_url = reverse_lazy('appartment:list_rooms')
    def get(self, request,booking_id=None,payment_id=None):
        payment =Payment.objects.get(id=payment_id)
        total_advance = Payment.objects.filter(booking=payment.booking,narration__in=['Advance Payment','Additional Payment']).aggregate(total=Sum('amount'))['total']
        return render(request, self.template_name,{'payment':payment,'advance':total_advance})     
    

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

        # Calculate opening and closing balances
        opening_balance = Transaction.get_opening_balance_for_date(current_date)
        closing_balance = Transaction.get_closing_balance_until_date(current_date)

        # Fetch transactions for the current date

        if 'all' in request.GET:
            transactions = Transaction.objects.all().order_by('date')
            filter='all'
            earliest_transaction = Transaction.objects.earliest('date').date
            latest_transaction = Transaction.objects.latest('date').date
            date_range = [earliest_transaction + timedelta(days=x) for x in range((latest_transaction - earliest_transaction).days + 1)]
            daily_balances = {day: {'opening': Transaction.get_opening_balance_for_date(day),
                        'closing': Transaction.get_closing_balance_until_date(day)}
                  for day in date_range}
        elif start_date is not None and end_date is not None:   
            filter = 'range'
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            date_range = [end_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
            daily_balances = {day: {'opening': Transaction.get_opening_balance_for_date(day),
                        'closing': Transaction.get_closing_balance_until_date(day)}
                  for day in date_range}
            transactions = Transaction.objects.filter(date__range=[start_date, end_date]).order_by('date')
        else:
            transactions = Transaction.objects.filter(date=current_date).order_by('date')

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
        return render(request, self.template_name)  
    
    def post(self, request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
                login(request, user)
                return redirect('appartment:dashboard') 
        else:   
                msg='Wrong Username or password'
        return render(request, self.template_name,{'msg':msg})  