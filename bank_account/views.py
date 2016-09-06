import re

from django.shortcuts import render, redirect
from .models import BankAccount, TransactionHistory, OPERATION, MAX_INCORRECT_PIN, ValidationError

enter_credential = 'Enter credentials'


def check_card_id(request):
    card_id = request.POST.get('card_id')
    if not card_id:
        return render(request, 'check_card_id.html')
    try:
        account = BankAccount.objects.get(card_id=card_id)
        if not account.is_blocked_card:
            request.session['card_id'] = card_id
            return render(request, 'check_pin.html', {'msg': 'Enter PIN'})
        else:
            return render(
                request, 'message.html', {
                    'msg': 'Account has been blocked'})
    except BankAccount.DoesNotExist:
        return render(request, 'message.html', {'msg': 'No such account'})


def check_pin(request):
    try:
        card_id = get_account(request)
    except KeyError:
        return render(request, 'message.html',
                      {'msg': enter_credential})
    user_pin = request.POST.get('pin')
    account = BankAccount.objects.get(card_id=card_id)
    if not account.is_blocked_pin and account.pin == user_pin:
        request.session['pin'] = account.pin
        return redirect('/transactions')

    elif not account.is_blocked_pin or account.incorrect_pin < MAX_INCORRECT_PIN:
        account.incorrect_pin += 1
        account.save()
        if account.incorrect_pin == MAX_INCORRECT_PIN:
            return render(
                request, 'message.html', {
                    'msg': 'Pin has been blocked'})

        return render(
            request, 'check_pin.html', {
                'msg': 'Incorrect pin: ' + str(
                    MAX_INCORRECT_PIN - account.incorrect_pin) + ' chance(s) left'})
    else:
        return render(request, 'message.html', {'msg': 'Pin is blocked'})


def balance(request):
    if not credential(request):
        return render(request, 'message.html', {'msg': enter_credential})
    card_id = get_account(request)
    account = BankAccount.objects.get(card_id=card_id)
    transaction = TransactionHistory(
        card_id=account,
        balance=account.balance,
        operation=OPERATION[0][0])
    transaction.save()
    return render(request, 'message.html', {
        'balance': BankAccount.objects.get(card_id=card_id).balance,
        'card_id': add_separator(card_id),
    })


def transactions(request):
    if not credential(request):
        return render(request, 'message.html', {'msg': enter_credential})

    card_id = get_account(request)
    account = BankAccount.objects.get(card_id=card_id)
    return render(request, 'transactions.html', {
        'transactions': account.transactionhistory_set.order_by('-date'),
        'card_id': add_separator(card_id),
        'balance': account.balance
    })


def money_withdrawal(request):
    if not credential(request):
        return render(request, 'message.html', {'msg': enter_credential})
    try:
        card_id = get_account(request)
        account = BankAccount.objects.get(card_id=card_id)
        withdrawal = request.POST.get('amount')
        if not withdrawal:
            return render(request, 'money_withdrawal.html', {
                'balance': account.balance})
        try:
            transaction = TransactionHistory(
                card_id=account,
                operation=OPERATION[1][0],
                money_withdrawal=int(withdrawal))
            transaction.save()
            return render(request, 'message.html', {
                'card_id': add_separator(card_id),
                'balance': account.balance,
                'msg': 'Withdrawal: {}'.format(withdrawal),
            })
        except ValidationError:
            return render(request, 'message.html', {
                'card_id': add_separator(card_id),
                'balance': account.balance,
                'msg': 'Amount exceeds the balance'
            })
    except ValueError:
        return render(
            request, 'money_withdrawal.html', {
                'msg': 'Only digits allowed'})


def get_account(request):
    return request.session['card_id']


def logout(request):
    request.session.flush()
    return redirect('/check_card_id')


def credential(request):
    return bool(request.session.get('card_id') and request.session.get('pin'))


def add_separator(string, sep='-'):
    return sep.join(re.findall('....', string))
