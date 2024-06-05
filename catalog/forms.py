from django import forms
from .models import MeterReading, Device, Division
from django.forms import ModelForm
from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class DateInput(forms.DateInput):
    input_type = 'date'

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    # device = forms.InlineForeignKeyField(Device.objects.all())
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if data < datetime.date.today():
            # raise ValidationError(_('Invalid date - renewal in past'))
            raise ValidationError('Invalid date - renewal in past')

        #Проверка того, то дата не выходит за "верхнюю" границу (+4 недели).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            # raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
            raise ValidationError('Invalid date - renewal more than 4 weeks ahead')

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data

# class NameModelChoiceField(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return "%s"%obj.name

# class MeterReadingCreateForm(ModelForm):

#     F_Division          = forms.ModelChoiceField(label='Цех', queryset=Division.objects.all())
#     # F_Devices           = forms.ModelChoiceField(label='Прибор', queryset=Device.objects.all())
#     # F_Tariff_Zones      = 
#     # N_Value             = 
#     # D_Date              = 
#     # F_Delivery_Methods  = 
#     # F_Creator           = 
#     # C_Notes             = 
#     # Img                 = 

#     class Meta:
#         model = MeterReading
#         fields = ['F_Division']#'__all__'#['title', 'description', 'made_on']
#     #     widgets = {
#     #         'D_Date': DateInput(),
#     #     }

class MeterReadingCreateForm(ModelForm):

    class Meta:
        model = MeterReading
        fields = '__all__'#['title', 'description', 'made_on']
        widgets = {
            'D_Date': DateInput(),
            # 'D_Date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class DeviceCreateForm(ModelForm):

    class Meta:
        model = Device
        fields = '__all__'#['title', 'description', 'made_on']
        widgets = {
            'D_Replace_Date': DateInput(),
            # 'D_Date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class DivisionCreateForm(ModelForm):

    class Meta:
        model = Division
        fields = '__all__'#['title', 'description', 'made_on']
        widgets = {
            'D_Date_Begin': DateInput(),
            'D_Date_End': DateInput(),
            # 'D_Date': forms.DateInput(attrs={'class': 'datepicker'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class DeviceUpdateForm(ModelForm):
    class Meta:
        model = Device
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class DivisionUpdateForm(ModelForm):
    class Meta:
        model = Division
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class MeterReadingUpdateForm(ModelForm):
    class Meta:
        model = MeterReading
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



        