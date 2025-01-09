from .models import *
from django import forms
from django.forms.widgets import DateTimeInput


class ConnectionForms(forms.ModelForm):
    class Meta:
        model = connections
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ConnectionForms, self).__init__(*args, **kwargs)
        # set password field invisible
        self.fields['password'].widget = forms.PasswordInput()






class service_timerForms(forms.ModelForm):
    class Meta:
        model = service_timer
        exclude = "__all__"
        labels = {
            'timeinterval': 'Time Interval in Minutes',
        }

class service_timerbyinterval(forms.ModelForm):
    class Meta:
        model = service_timer
        fields = ['timeinterval']
        labels = {
            'timeinterval': 'Time Interval in Minutes',
        }


class service_timerHourlyForms(forms.ModelForm):
    class Meta:
        model = service_timer
        fields = ['minutes_for_hour']
        labels = {
            'minutes_for_hour': 'Job time (every hour)',
        }
        help_texts = {
            'minutes_for_hour': 'Enter the time for the job to run every hour. example: 1--59',
        }

class service_timerDailyForms(forms.ModelForm):
    class Meta:
        model = service_timer
        fields = ['time_for_day']
        labels = {
            'time_for_day': 'Job time (every Day)',
        }
        widgets = {
            'time_for_day': forms.TimeInput(attrs={'type': 'time'})
        }
        help_texts = {
            'time_for_day': 'Enter the time for the job to run every day.',
        }



class service_timerWeeklyForms(forms.ModelForm):
    class Meta:
        model = service_timer
        fields = ['day_name_for_week', 'time_for_week']
        labels = {
            'time_for_week': 'Job time (every Day)',
            'day_name_for_week': 'Day'
        }
        help_texts = {
            'time_for_week': 'Enter the time for the job to run every week.',
            'day_name_for_week':'Enter day name for the job to run every week'
        }
        widgets = {
            'time_for_week': forms.TimeInput(attrs={'type': 'time'})
        }

class ExcludeSeconds(DateTimeInput):
    # format = '%Y-%m-%dT%H:%M'
    format = '%d-%m-%YT%H:%M'


class SchedulesForms(forms.ModelForm):
    class Meta:
        model = Jobs

        exclude = ['run_separate']
        widgets = {
            'start_task': ExcludeSeconds(attrs={'type': 'datetime-local'}),
            'end_task': ExcludeSeconds(attrs={'type': 'datetime-local'}),
            'last_executed': ExcludeSeconds(attrs={'type': 'date-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(SchedulesForms, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['active'].widget.attrs.update({'class': 'form-check-input'})


