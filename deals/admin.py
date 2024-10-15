from django.contrib import admin

from .models import DealsSector, Deals, FavoriteDeals, Contact,  Country, PaymentCondition

admin.site.register(DealsSector)
admin.site.register(Deals)
admin.site.register(FavoriteDeals)
admin.site.register(Contact)
admin.site.register(Country)
admin.site.register(PaymentCondition)

