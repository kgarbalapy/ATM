from django.conf.urls import url
from django.contrib import admin

from bank_account.views import check_card_id, check_pin, balance, money_withdrawal, transactions, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^check_card_id', check_card_id),
    url(r'^check_pin', check_pin),
    url(r'^transactions', transactions),
    url(r'^balance', balance),
    url(r'^money_withdrawal', money_withdrawal),
    url(r'^logout', logout),
]
