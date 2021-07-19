from django import forms
from django.utils.translation import gettext_lazy as _
from .models import District, Sector, Cell

class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.currentUser = kwargs.pop('currentUser', None)
        super(UserForm, self).__init__(*args, **kwargs)

    category_choices = (
        ('extarnal-teritory', _("TERITORY MANAGER")),
        ('sales-agent', _("SALES AGENT")),
    )
    
    gender_choices = (
        ('m', _("Male")),
        ('f', _("Female")),
    )
    
    first_name = forms.CharField(label='First name', required=False)
    last_name = forms.CharField(label='Last name')
    category = forms.ChoiceField(label='Category',choices=category_choices, required=False)
    gender = forms.ChoiceField(label='Gender', choices=gender_choices, required=False)
    email = forms.EmailField(label='Email', required=True)
    phone = forms.IntegerField(label='Phone No', min_value=0)
    district = forms.ModelChoiceField(label='Districit',queryset=District.objects.all())
    sector = forms.ModelChoiceField(label='Sector',queryset=Sector.objects.all())
    cell = forms.ModelChoiceField(label='Cell',queryset=Cell.objects.all())
    tin = forms.IntegerField(label='TIN Number', min_value=0)
    nid = forms.IntegerField(label='National ID', min_value=0)
    
    first_name.widget.attrs.update({'class':'r-form-1-first-name form-control', 'placeholder':'Enter first name'})
    last_name.widget.attrs.update({'class':'r-form-1-last-name form-control', 'placeholder':'Enter last name'})
    email.widget.attrs.update({'class':'r-form-1-last-name form-control', 'placeholder':'Enter email'})
    category.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'select category'})
    district.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'select district'})
    sector.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'select sector'})
    cell.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'select sector'})
    gender.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'select your gender'})
    tin.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'Enter your TIN Number'})
    phone.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'Enter your phone number'})
    nid.widget.attrs.update({'class':'r-form-1-email form-control', 'placeholder':'Enter your nationa ID NO'})

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
