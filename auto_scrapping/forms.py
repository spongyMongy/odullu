from django import forms
from .models import *
from durationwidget.widgets import TimeDurationWidget


class GiftModelUserForm(forms.ModelForm):
    # link = forms.DurationField(
    #     widget=TimeDurationWidget(show_days=False, show_hours=True,
    #                               show_minutes=True, show_seconds=False),
    #     required=False)
    # time = forms.DurationField(
    #     widget=TimeDurationWidget(show_days=False, show_hours=True,
    #                               show_minutes=True, show_seconds=False),
    #     required=False)

    class Meta:
        model = GiftModelUserEntry
        fields = '__all__'
        exclude = ( 'username', 'picture', 'time', 'thumbnail_link',)
