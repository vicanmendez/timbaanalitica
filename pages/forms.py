from django import forms

   
class ConsultaForm(forms.Form):
    dates = forms.DateField(widget=forms.DateInput(attrs={'id':'datepicker', 'class':'form-control', 'placeholder':'Seleccione las fechas a estudiar', 'required':'True'}))
