from django import forms

   
class ConsultaForm(forms.Form):
    dates = forms.DateField(widget=forms.DateInput(attrs={'id':'datepicker', 'class':'form-control', 'placeholder':'Seleccione las fechas a estudiar', 'required':'True'}), label="Selecciona las fechas:")
    typeFilter = forms.ChoiceField(choices=[('1', 'Ver los más salidores'), ('2', 'Ver números atrasados o menos salidores')], widget=forms.Select(attrs={'class':'form-control', 'required':'True'}), label="¿Preferencias por salidores?")
    numberFilter = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Ej: Para ver el top 10 sólo ingresa 10', 'required':'True'}), label="¿Cuántos números quieres ver?")