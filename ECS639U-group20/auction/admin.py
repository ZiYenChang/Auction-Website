from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Item, Question, Answer, Bid


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_of_birth", "city", "is_staff", "is_active", "date_joined")

admin.site.register(User, UserAdmin)
admin.site.register(Item)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Bid)