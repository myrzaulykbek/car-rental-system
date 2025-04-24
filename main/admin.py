from django.contrib import admin
from .models import User, Car, Rental, Payment

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    list_filter = ['role', 'is_staff']
    search_fields = ['username', 'email']

admin.site.register(User, UserAdmin)
admin.site.register(Car)
admin.site.register(Rental)
admin.site.register(Payment)


from .models import Booking, Review

admin.site.register(Booking)

admin.site.register(Review)


