# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-06 18:33
from __future__ import unicode_literals

import bank_account.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(max_length=16, unique=True, validators=[bank_account.models.only_integers, django.core.validators.MinLengthValidator(16)])),
                ('is_blocked_card', models.BooleanField(default=False)),
                ('pin', models.CharField(max_length=4, validators=[bank_account.models.only_integers, django.core.validators.MinLengthValidator(4)])),
                ('is_blocked_pin', models.BooleanField(default=False)),
                ('incorrect_pin', models.SmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0)),
                ('balance', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'bank_account',
            },
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(choices=[('0', 'balance'), ('1', 'money withdrawal')], max_length=20)),
                ('balance', models.IntegerField(blank=True, editable=False, null=True)),
                ('money_withdrawal', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank_account.BankAccount')),
            ],
            options={
                'db_table': 'transaction',
                'verbose_name_plural': 'Transactions history',
            },
        ),
    ]
