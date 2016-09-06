from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _

ID_LENGTH = 16
PIN_LENGTH = 4
MAX_INCORRECT_PIN = 4
CHOICES = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
)

OPERATION = (
    ('0', 'balance'),
    ('1', 'money withdrawal'),
)


def only_integers(value):
    if not value.isdigit():
        raise ValidationError(
            _('only integers allowed')
        )


class BankAccount(models.Model):
    card_id = models.CharField(unique=True, max_length=ID_LENGTH, validators=[
                               only_integers, MinLengthValidator(ID_LENGTH)])
    is_blocked_card = models.BooleanField(default=False)
    pin = models.CharField(
        max_length=4,
        validators=[
            only_integers,
            MinLengthValidator(PIN_LENGTH)])
    is_blocked_pin = models.BooleanField(default=False)
    incorrect_pin = models.SmallIntegerField(default=0, choices=CHOICES)
    balance = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.incorrect_pin >= MAX_INCORRECT_PIN:
            self.is_blocked_pin = True
        else:
            self.is_blocked_pin = False
        self.full_clean()
        return super(BankAccount, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{0}'.format(self.card_id)

    class Meta:
        db_table = 'bank_account'


class TransactionHistory(models.Model):
    card_id = models.ForeignKey(BankAccount)
    operation = models.CharField(max_length=20, choices=OPERATION)
    balance = models.IntegerField(null=True, blank=True, editable=False)
    money_withdrawal = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def validate_withdrawal(self):
        if not self.money_withdrawal:
            return
        if self.money_withdrawal > self.card_id.balance:
            raise ValidationError(
                _('amount exceeds the balance')
            )
        self.card_id.balance -= self.money_withdrawal
        self.balance = self.card_id.balance
        self.card_id.save()

    def save(self, *args, **kwargs):
        self.validate_withdrawal()
        super(TransactionHistory, self).save(*args, **kwargs)

    class Meta:
        db_table = 'transaction'
        verbose_name_plural = 'Transactions history'
