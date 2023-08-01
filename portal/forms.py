from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from patients.models import Patient, Cases
from doctors.models import Doctor


# Overriding the default authentication form
class AuthForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-input',
                                                           'id': 'username',
                                                           'placeholder': 'username',
                                                           'autofocus': ''}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-input',
                                          'id': 'password',
                                          'placeholder': 'password',
                                          'autofocus': ''}))


# Creating new patient form
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input',
                                           'id': 'name',
                                           'placeholder': 'Name',
                                           'autofocus': ''}),
            'age': forms.NumberInput(attrs={'class': 'form-input',
                                            'id': 'age',
                                            'placeholder': '100',
                                            'min': 0,
                                            'max': 150,
                                            'autofocus': ''}),
            'gender': forms.Select(choices=Patient.gender_list, attrs={'class': 'form-input-dropdown',
                                                                       'id': 'gender',
                                                                       'autofocus': ''}),
            'blood_type': forms.Select(choices=Patient.blood_types, attrs={'class': 'form-input-dropdown',
                                                                           'id': 'blood_type',
                                                                           'autofocus': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-input',
                                             'id': 'email',
                                             'placeholder': 'example@email.com',
                                             'autofocus': ''}),
            'phone': forms.NumberInput(attrs={'class': 'form-input',
                                              'id': 'phone',
                                              'min': 1000000000,
                                              'max': 9999999999,
                                              'placeholder': '1234567890',
                                              'autofocus': ''})
        }


# Case Creation form
class CaseCreationForm(forms.Form):

    patient = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-input-dropdown',
                                                           'id': 'patient',
                                                           'autofocus': ''}))
    doctor = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-input-dropdown',
                                                          'id': 'docotr',
                                                          'autofocus': ''}))
    state = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-input-dropdown',
                                                         'id': 'docotr',
                                                         'autofocus': ''}))
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                               widget=forms.DateTimeInput(attrs={'class': 'form-input',
                                                                 'id': 'name',
                                                                 'placeholder': 'DD/MM/YYYY HH:MM',
                                                                 'autofocus': ''}))

    def set_choices(self):

        # Getting the list of available doctors that day
        doctors = Doctor.objects.filter(availability=True)
        doctor_list = []

        # Checking if the doctors are free
        for doctor in doctors:
            if doctor.cases_set.filter(status='t').count() < 10:
                doctor_list.append((doctor.id, doctor.user.user.username))

        # Setting the values for choices
        self.fields["patient"].choices = ((patient.id, f"ID: {patient.id} | Name: {patient.name}") for patient in Patient.objects.all())
        self.fields["doctor"].choices = doctor_list
        self.fields["state"].choices = Cases.states


class CaseEditForm(CaseCreationForm):
    patient = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-input-dropdown',
                                                           'id': 'patient',
                                                           'autofocus': '',
                                                           'readonly': ""}))

    def set_patient(self, patients):
        self.fields["patient"].choices = [(patient.id, f"ID: {patient.id} | Name: {patient.name}") for patient in patients]
