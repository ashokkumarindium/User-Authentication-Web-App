from django.db.models.fields import DateField
from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  get_user_model
from django.contrib import messages
from .forms import UserRegistration, UserEditForm

from .models import Person,Transactions
import datetime
@login_required
def dashboard(request):
    transactions = Transactions.objects.all().filter(user_name=request.user.username)
    context = {}
    context['transactions'] = transactions
    if transactions==None:
        context['balance'] = 1000
    else:
        balance = find_balance(transactions)
        # balance = 1000
        # for transaction in transactions:
        #     if transaction.type == 'CREDIT':
        #         balance = balance + transaction.amount
        #     else: 
        #         balance = balance - transaction.amount
        context['balance'] = balance
    return render(request, 'authapp/dashboard.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)


@login_required
def clearall(request):
    Transactions.objects.all().delete()

    context = {}
    return render(request, 'authapp/dashboard.html', context=context)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)


@login_required
def transfer(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    User = get_user_model()
    users = User.objects.all()
    context['users'] = users
    return render(request, 'authapp/transfer.html', context=context)


@login_required
def initiatetransfer(request):
    if request.method == 'POST':
        transaction_data = request.POST
        if transaction_data['transaction_amount']=="" or transaction_data['transaction_description']=="":
            message='some or all of the inputs incorrect'
            transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
            context = {}
            context['message'] = message
            context['transactions'] = transactions_opbj
            if transactions_opbj==None:
                context['balance'] = 1000
            else:
                balance = find_balance(transactions_opbj)
                # balance = 1000
                # for transaction in transactions_opbj:
                #     if transaction.type == 'CREDIT':
                #         balance = balance + transaction.amount
                #     else: 
                #         balance = balance - transaction.amount
                context['balance'] = balance
            return render(request, 'authapp/dashboard.html', context=context)

        transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
        balance = find_balance(transactions_opbj)
        # balance = 1000
        # for transaction in transactions_opbj:
        #     if transaction.type == 'CREDIT':
        #         balance = balance + transaction.amount
        #     else: 
        #         balance = balance - transaction.amount
        balance = balance - float(transaction_data['transaction_amount'])

        if balance<0:
            message='You cannot transfer amount greater than your wallet balance'
            transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
            context = {}
            context['message'] = message
            context['transactions'] = transactions_opbj
            if transactions_opbj==None:
                context['balance'] = 1000
            else:
                balance = find_balance(transactions_opbj)
                # balance = 1000
                # for transaction in transactions_opbj:
                #     if transaction.type == 'CREDIT':
                #         balance = balance + transaction.amount
                #     else: 
                #         balance = balance - transaction.amount
                context['balance'] = balance
            return render(request, 'authapp/dashboard.html', context=context)
        
        a = Transactions(user_name = request.user.username,
        
                        transaction_date =datetime.datetime.today(),
                        description = transaction_data['transaction_description'],
                        type =  transaction_data['transaction_type'],
                        amount = transaction_data['transaction_amount'],
                        balance = balance
                        )
        a.save()

        transactions_opbj = Transactions.objects.all().filter(user_name=transaction_data['benificiary'])
        print(transactions_opbj)
        balance = find_balance(transactions_opbj)
        # balance = 1000
        # for transaction in transactions_opbj:
        #     if transaction.type == 'CREDIT':
        #         balance = balance + transaction.amount
        #     else: 
        #         balance = balance - transaction.amount
        balance = balance + float(transaction_data['transaction_amount'])

        b = Transactions(user_name = transaction_data['benificiary'],
                        transaction_date =datetime.datetime.today(),
                        description = transaction_data['transaction_description'],
                        type =  'CREDIT',
                        amount = transaction_data['transaction_amount'],
                        balance = balance
                        )
        b.save()
        transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
        context = {}
        context['transactions'] = transactions_opbj
        if transactions_opbj==None:
            context['balance'] = 1000
        else:
            balance = find_balance(transactions_opbj)
            # balance = 1000
            # for transaction in transactions_opbj:
            #     if transaction.type == 'CREDIT':
            #         balance = balance + transaction.amount
            #     else: 
            #         balance = balance - transaction.amount
            context['balance'] = balance
        return render(request, 'authapp/dashboard.html', context=context)
    


@login_required
def new_transaction(request):
    if request.method == 'POST':
        transaction_data = request.POST
        if transaction_data['transaction_date'] == "" or transaction_data['transaction_amount']=="" or transaction_data['transaction_description']=="":
            message='some or all of the inputs incorrect'
            transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
            context = {}
            context['message'] = message
            context['transactions'] = transactions_opbj
            if transactions_opbj==None:
                context['balance'] = 1000
            else:
                balance = find_balance(transactions_opbj)
                # balance = 1000
                # for transaction in transactions_opbj:
                #     if transaction.type == 'CREDIT':
                #         balance = balance + transaction.amount
                #     else: 
                #         balance = balance - transaction.amount
                context['balance'] = balance
            return render(request, 'authapp/dashboard.html', context=context)

        transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
        balance = find_balance(transactions_opbj)
        # balance = 1000
        # for transaction in transactions_opbj:
        #     if transaction.type == 'CREDIT':
        #         balance = balance + transaction.amount
        #     else: 
        #         balance = balance - transaction.amount
        
        if transaction_data['transaction_type'] == 'CREDIT':
            balance = balance + float(transaction_data['transaction_amount'])
        else:
            balance = balance - float(transaction_data['transaction_amount'])

        if balance<0:
            message='You have exceeded the coupon amount'
            transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
            context = {}
            context['message'] = message
            context['transactions'] = transactions_opbj
            if transactions_opbj==None:
                context['balance'] = 1000
            else:
                balance = find_balance(transactions_opbj)
                # balance = 1000
                # for transaction in transactions_opbj:
                #     if transaction.type == 'CREDIT':
                #         balance = balance + transaction.amount
                #     else: 
                #         balance = balance - transaction.amount
                context['balance'] = balance
            return render(request, 'authapp/dashboard.html', context=context)

        a = Transactions(user_name = request.user.username,
                        transaction_date =transaction_data['transaction_date'],
                        description = transaction_data['transaction_description'],
                        type =  transaction_data['transaction_type'],
                        amount = transaction_data['transaction_amount'],
                        balance = balance
                        )
        a.save()
        transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
        context = {}
        context['transactions'] = transactions_opbj
        if transactions_opbj==None:
            context['balance'] = 1000
        else:
            balance = find_balance(transactions_opbj)
            # balance = 1000
            # for transaction in transactions_opbj:
            #     if transaction.type == 'CREDIT':
            #         balance = balance + transaction.amount
            #     else: 
            #         balance = balance - transaction.amount
            context['balance'] = balance
        return render(request, 'authapp/dashboard.html', context=context)
    else:
        transactions_opbj = Transactions.objects.all().filter(user_name=request.user.username)
        context = {}
        context['transactions'] = transactions_opbj
        if transactions_opbj==None:
            context['balance'] = 1000
        else:
            balance = find_balance(transactions_opbj)
            # balance = 1000
            # for transaction in transactions_opbj:
            #     if transaction.type == 'CREDIT':
            #         balance = balance + transaction.amount
            #     else: 
            #         balance = balance - transaction.amount

            context['balance'] = balance
        return render(request, 'authapp/dashboard.html', context=context)


def find_balance(transactions):
    balance = 1000
    for transaction in transactions:
            if transaction.type == 'CREDIT':
                balance = balance + transaction.amount
            else: 
                balance = balance - transaction.amount
    return balance