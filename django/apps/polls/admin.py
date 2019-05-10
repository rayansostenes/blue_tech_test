from django.db import models
from django.forms import TextInput
from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.StackedInline):
    model = Choice
    formfield_overrides = {
        models.TextField: {'widget': TextInput},
    }

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

@admin.register(Vote)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'poll', 'choice']