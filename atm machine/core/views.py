from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from core.forms import *


@login_required
def home(request):
    return render(request, 'home.html')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('forms')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        deposit.user.account.balance += deposit.amount
        deposit.user.account.save()
        messages.success(request, 'You Have Deposited {} Rs.'
                         .format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "form.html", context)


@login_required()
def withdrawal_view(request):
    form = WithdrawalForm(request.POST or None, user=request.user)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.save()
        # subtracts users withdrawal from balance.
        withdrawal.user.account.balance -= withdrawal.amount
        withdrawal.user.account.save()

        messages.success(
            request, 'You Have Withdrawn {} Rs.'.format(withdrawal.amount)
        )
        return redirect("home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "form.html", context)


