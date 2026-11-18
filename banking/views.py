from decimal import Decimal
from django.contrib import messages
from django.db import transaction as db_transaction
from .models import Wallet, Transaction
from .forms import (
    TransferForm,
    AirtimeForm,
    DataBundleForm,
    ElectricityForm,
    ProfileUpdateForm,
    TVSubscriptionForm,
    WaterBillForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'banking/register.html', {'form': form})


# Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'banking/login.html', {'form': form})


# Dashboard
@login_required(login_url='login')
def dashboard(request):

    wallet, created = Wallet.objects.get_or_create(
        user=request.user
    )

    transactions = Transaction.objects.filter(
        sender=request.user
    ).order_by('-created_at')

    context = {
        'username': request.user.username,
        'account_number': '1234567890',
        'balance': wallet.balance,
        'transactions': transactions
    }

    return render(
        request,
        'banking/dashboard.html',
        context
    )
# Logout
def user_logout(request):
    if request.method == 'POST':
        logout(request)

    return redirect('login')
# Money Transfer Page
@login_required(login_url='login')
def transfer(request):

    wallet, created = Wallet.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = TransferForm(request.POST)

        if form.is_valid():

            amount = form.cleaned_data['amount']

            if amount > wallet.balance:
                messages.error(
                    request,
                    "Insufficient demo wallet balance."
                )

            else:

                request.session['transfer_details'] = {
                    'recipient_name': form.cleaned_data['recipient_name'],
                    'bank_name': form.cleaned_data['bank_name'],
                    'account_number': form.cleaned_data['account_number'],
                    'amount': str(amount)
                }

                return redirect('transfer_review')

    else:
        form = TransferForm()

    return render(
        request,
        'banking/transfer.html',
        {
            'form': form,
            'balance': wallet.balance
        }
    )


# Transfer Review Page
@login_required(login_url='login')
def transfer_review(request):

    details = request.session.get('transfer_details')

    if not details:
        return redirect('transfer')

    return render(
        request,
        'banking/transfer_review.html',
        {'details': details}
    )


# Confirm Transfer
@login_required(login_url='login')
def confirm_transfer(request):

    if request.method != 'POST':
        return redirect('transfer')

    details = request.session.get('transfer_details')

    if not details:
        return redirect('transfer')

    amount = Decimal(details['amount'])

    with db_transaction.atomic():

        wallet = Wallet.objects.select_for_update().get(
            user=request.user
        )

        if amount <= 0 or amount > wallet.balance:
            messages.error(
                request,
                "Transfer could not be completed. Check your balance."
            )
            return redirect('transfer')

        wallet.balance -= amount
        wallet.save()

        new_transaction = Transaction.objects.create(
            sender=request.user,
            recipient_name=details['recipient_name'],
            bank_name=details['bank_name'],
            account_number=details['account_number'],
            amount=amount,
            status='Successful',
            transaction_type='Transfer'
        )

    del request.session['transfer_details']

    messages.success(
        request,
        "Your simulated transfer was successful!"
    )

    return redirect(
        'transaction_receipt',
        transaction_id=new_transaction.id
    )
# Transaction History Page
@login_required(login_url='login')
def transaction_history(request):

    transactions = Transaction.objects.filter(
        sender=request.user
    ).order_by('-created_at')

    return render(
        request,
        'banking/transaction_history.html',
        {'transactions': transactions}
    )
@login_required(login_url='login')
def airtime(request):

    wallet, created = Wallet.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = AirtimeForm(request.POST)

        if form.is_valid():

            amount = form.cleaned_data['amount']

            if amount > wallet.balance:

                messages.error(
                    request,
                    "Insufficient demo wallet balance."
                )

            else:

                request.session['airtime_details'] = {
                    'network': form.cleaned_data['network'],
                    'phone_number': form.cleaned_data['phone_number'],
                    'amount': str(amount)
                }

                return redirect('airtime_review')

    else:

        form = AirtimeForm()

    return render(
        request,
        'banking/airtime.html',
        {
            'form': form,
            'balance': wallet.balance
        }
    )
@login_required(login_url='login')
def airtime_review(request):

    details = request.session.get('airtime_details')

    if not details:
        return redirect('airtime')

    return render(
        request,
        'banking/airtime_review.html',
        {'details': details}
    )

@login_required(login_url='login')
def confirm_airtime(request):

    if request.method != 'POST':
        return redirect('airtime')

    details = request.session.get('airtime_details')

    if not details:
        return redirect('airtime')

    amount = Decimal(details['amount'])

    with db_transaction.atomic():

        wallet = Wallet.objects.select_for_update().get(
            user=request.user
        )

        if amount < Decimal('50.00') or amount > wallet.balance:

            messages.error(
                request,
                "Airtime purchase could not be completed."
            )

            return redirect('airtime')

        wallet.balance -= amount
        wallet.save()

        new_transaction = Transaction.objects.create(
            sender=request.user,
            transaction_type='Airtime',
            recipient_name=details['phone_number'],
            bank_name=details['network'],
            account_number=details['phone_number'],
            amount=amount,
            status='Successful'
        )

    del request.session['airtime_details']

    messages.success(
        request,
        "Your simulated airtime purchase was successful!"
    )

    return redirect(
        'transaction_receipt',
        transaction_id=new_transaction.id
    )

@login_required(login_url='login')
def data_bundle(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = DataBundleForm(request.POST)

        if form.is_valid():
            plans = {
                '500MB': Decimal('500'),
                '1GB': Decimal('1000'),
                '2GB': Decimal('2000'),
                '5GB': Decimal('4000'),
                '10GB': Decimal('8000'),
            }

            data_plan = form.cleaned_data['data_plan']
            amount = plans[data_plan]

            if amount > wallet.balance:
                messages.error(request, 'Insufficient wallet balance.')
            else:
                request.session['data_details'] = {
                    'network': form.cleaned_data['network'],
                    'phone_number': form.cleaned_data['phone_number'],
                    'data_plan': data_plan,
                    'amount': str(amount),
                }

                return redirect('data_review')
    else:
        form = DataBundleForm()

    return render(request, 'banking/data_bundle.html', {
        'form': form,
        'balance': wallet.balance,
    })


@login_required(login_url='login')
def data_review(request):
    details = request.session.get('data_details')

    if not details:
        return redirect('data_bundle')

    return render(request, 'banking/data_review.html', {
        'details': details
    })


@login_required(login_url='login')
def confirm_data(request):

    if request.method != 'POST':
        return redirect('data_bundle')

    details = request.session.get('data_details')

    if not details:
        return redirect('data_bundle')

    amount = Decimal(details['amount'])

    with db_transaction.atomic():

        wallet = Wallet.objects.select_for_update().get(
            user=request.user
        )

        if amount <= 0 or amount > wallet.balance:
            messages.error(
                request,
                'Insufficient wallet balance.'
            )
            return redirect('data_bundle')

        wallet.balance -= amount
        wallet.save()

        new_transaction = Transaction.objects.create(
            sender=request.user,
            transaction_type='Data',
            recipient_name=details['phone_number'],
            bank_name=details['network'],
            account_number=details['phone_number'],
            amount=amount,
            status='Successful'
        )

    del request.session['data_details']

    messages.success(
        request,
        'Your simulated data purchase was successful!'
    )

    return redirect(
        'transaction_receipt',
        transaction_id=new_transaction.id
    )

@login_required(login_url='login')
def electricity(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ElectricityForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount > wallet.balance:
                messages.error(request, 'Insufficient wallet balance.')
            else:
                request.session['electricity_details'] = {
                    'provider': form.cleaned_data['provider'],
                    'meter_type': form.cleaned_data['meter_type'],
                    'meter_number': form.cleaned_data['meter_number'],
                    'amount': str(amount),
                }

                return redirect('electricity_review')
    else:
        form = ElectricityForm()

    return render(request, 'banking/electricity.html', {
        'form': form,
        'balance': wallet.balance,
    })


@login_required(login_url='login')
def electricity_review(request):
    details = request.session.get('electricity_details')

    if not details:
        return redirect('electricity')

    return render(request, 'banking/electricity_review.html', {
        'details': details
    })

@login_required(login_url='login')
def confirm_electricity(request):

    if request.method != 'POST':
        return redirect('electricity')

    details = request.session.get('electricity_details')

    if not details:
        return redirect('electricity')

    amount = Decimal(details['amount'])

    with db_transaction.atomic():

        wallet = Wallet.objects.select_for_update().get(
            user=request.user
        )

        if amount < Decimal('500') or amount > wallet.balance:
            messages.error(
                request,
                'Invalid amount or insufficient balance.'
            )
            return redirect('electricity')

        wallet.balance -= amount
        wallet.save()

        new_transaction = Transaction.objects.create(
            sender=request.user,
            transaction_type='Electricity',
            recipient_name=details['meter_number'],
            bank_name=details['provider'],
            account_number=details['meter_number'],
            amount=amount,
            status='Successful'
        )

    del request.session['electricity_details']

    messages.success(
        request,
        'Your simulated electricity payment was successful!'
    )

    return redirect(
        'transaction_receipt',
        transaction_id=new_transaction.id
    )


@login_required(login_url='login')
def profile(request):
    wallet, created = Wallet.objects.get_or_create(
        user=request.user
    )

    return render(request, 'banking/profile.html', {
        'user': request.user,
        'wallet': wallet,
    })
@login_required(login_url='login')
def update_profile(request):

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'banking/update_profile.html', {
        'form': form
    })
@login_required(login_url='login')
def tv_subscription(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = TVSubscriptionForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount > wallet.balance:
                messages.error(request, 'Insufficient wallet balance.')
            else:
                request.session['tv_details'] = {
                    'provider': form.cleaned_data['provider'],
                    'smartcard_number': form.cleaned_data['smartcard_number'],
                    'package': form.cleaned_data['package'],
                    'amount': str(amount),
                }

                return redirect('tv_review')
    else:
        form = TVSubscriptionForm()

    return render(request, 'banking/tv_subscription.html', {
        'form': form,
        'balance': wallet.balance,
    })


@login_required(login_url='login')
def tv_review(request):
    details = request.session.get('tv_details')

    if not details:
        return redirect('tv_subscription')

    return render(request, 'banking/tv_review.html', {
        'details': details
    })

@login_required(login_url='login')
def confirm_tv(request):

    if request.method != 'POST':
        return redirect('tv_subscription')

    details = request.session.get('tv_details')

    if not details:
        return redirect('tv_subscription')

    amount = Decimal(details['amount'])

    with db_transaction.atomic():

        wallet = Wallet.objects.select_for_update().get(
            user=request.user
        )

        if amount < Decimal('500') or amount > wallet.balance:
            messages.error(
                request,
                'Invalid amount or insufficient balance.'
            )
            return redirect('tv_subscription')

        wallet.balance -= amount
        wallet.save()

        new_transaction = Transaction.objects.create(
            sender=request.user,
            transaction_type='TV Subscription',
            recipient_name=details['smartcard_number'],
            bank_name=details['provider'],
            account_number=details['smartcard_number'],
            amount=amount,
            status='Successful'
        )

    del request.session['tv_details']

    messages.success(
        request,
        'Your simulated TV subscription payment was successful!'
    )

    return redirect(
        'transaction_receipt',
        transaction_id=new_transaction.id
    )


@login_required(login_url='login')
def water_bill(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = WaterBillForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount > wallet.balance:
                messages.error(request, 'Insufficient wallet balance.')
            else:
                request.session['water_details'] = {
                    'provider': form.cleaned_data['provider'],
                    'customer_number': form.cleaned_data['customer_number'],
                    'amount': str(amount),
                }

                return redirect('water_review')
    else:
        form = WaterBillForm()

    return render(request, 'banking/water_bill.html', {
        'form': form,
        'balance': wallet.balance,
    })


@login_required(login_url='login')
def water_review(request):
    details = request.session.get('water_details')

    if not details:
        return redirect('water_bill')

    return render(request, 'banking/water_review.html', {
        'details': details
    })

@login_required(login_url='login')
def confirm_water(request):

    if request.method != 'POST':
        return redirect('water_bill')

    details = request.session.get('water_details')

    if not details:
        return redirect('water_bill')

    amount = Decimal(details['amount'])

    with db_transaction.atomic():

        wallet = Wallet.objects.select_for_update().get(
            user=request.user
        )

        if amount < Decimal('500') or amount > wallet.balance:
            messages.error(
                request,
                'Invalid amount or insufficient balance.'
            )
            return redirect('water_bill')

        wallet.balance -= amount
        wallet.save()

        new_transaction = Transaction.objects.create(
            sender=request.user,
            transaction_type='Water Bill',
            recipient_name=details['customer_number'],
            bank_name=details['provider'],
            account_number=details['customer_number'],
            amount=amount,
            status='Successful'
        )

    del request.session['water_details']

    messages.success(
        request,
        'Your simulated water bill payment was successful!'
    )

    return redirect(
        'transaction_receipt',
        transaction_id=new_transaction.id
    )


@login_required(login_url='login')
def transaction_receipt(request, transaction_id):

    receipt = get_object_or_404(
        Transaction,
        id=transaction_id,
        sender=request.user,
        status='Successful'
    )

    context = {
        'receipt': receipt
    }

    return render(
        request,
        'banking/transaction_receipt.html',
        context
    )