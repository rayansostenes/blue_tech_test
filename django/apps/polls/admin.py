from django.contrib import admin
from .models import Poll, Choice, Response

class ChoiceInline(admin.TabularInline):
    model = Choice

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'poll', 'choice']