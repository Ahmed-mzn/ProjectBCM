from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Compte)
admin.site.register(CarnetCheque)
admin.site.register(Cheque)
admin.site.register(CarnetBV)
admin.site.register(ChequeBV)