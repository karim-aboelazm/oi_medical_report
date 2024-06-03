from django import forms
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
from .models import Patient
from django.contrib.auth.models import User

def get_text_form_report(file:str=None):
    data = []
    if file is not None:
        if str(file).endswith('.pdf'):
            doc = DocumentFile.from_pdf(file)
        else:
            doc = DocumentFile.from_images(file)
        predictor = ocr_predictor(pretrained=True)
        result = predictor(doc).export()
        blocks = result['pages'][0]['blocks']
        for block in blocks:
            lines_of_words = block['lines'][0]['words']
            for word in lines_of_words:
                data.append(word)
    return data

def group_words_by_geometry_y(data,tol=0.09):
    grouped_words, lines, last_data = [],[],[]
    for entry in data:
        y_center = (entry['geometry'][0][1] + entry['geometry'][1][1]) / 2
        added = False
        for group in grouped_words:
            if abs(y_center - group[0]['geometry'][0][1]) <= tol:
                group.append(entry)
                added = True
                break
        if not added:
            grouped_words.append([entry])
            
    for group in grouped_words:
        words = [word['value'] for word in group]
        lines.append(words)
        
    for line in lines:
        d = {"name":"","min_value":0,"current_value":0,"max_value":0}
        nums = []
        for item in line:
            if item.isalpha():
                d['name'] += item + " "
            if item.replace('.','',1).isdigit():
                nums.append(float(item))
            if nums and len(nums) > 0:
                d['min_value'] = min(nums)
                d['max_value'] = max(nums)
                d['current_value'] = next((x for x in nums if d['min_value'] < x < d['max_value']),None)
        d['name'] = d['name'].strip()
        last_data.append(d)
    return last_data

class MedicalReportReaderForm(forms.Form):
    input_file = forms.FileField()
    def get_file_data(self):
        file_path = self.cleaned_data['input_file']
        if not str(file_path).endswith('.pdf'):
            file_path = file_path.read()
        data = get_text_form_report(file_path)
        final_output = group_words_by_geometry_y(data)
        return final_output
    
class PatientRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Patient
        fields = [
            'username',
            'full_name',
            'email',
            'password',
            'phone',
            'address',
        ]
        
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError('Patient with this username is already exists ! please try again :( ')
        return user_name

class PatientLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        user_name = self.cleaned_data['username']
        if User.objects.filter(username=user_name).exists():
            return user_name
        else:
            raise forms.ValidationError('Patient with this username does not exist. Please try again.')

class PatientUpdateForm(forms.ModelForm):
    class Meta:
       model = Patient
       fields = [
           'full_name',
           'address',
           'phone',
           'image',
           ]

class PatientForgetPasswordForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Your Email Here ...'
    }))
    def clean_email(self):
        e = self.cleaned_data.get('email')
        if Patient.objects.filter(user__email = e).exists():
            pass
        else:
            raise forms.ValidationError('Patient With This Email Does Not Exists.')
        return e
    
class PatientResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Enter Your New password'
    }),label='New Password')
    
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Confirm Your New password'
    }),label='Confirm New Password')
    
    def clean_confirmation_new_password(self):
        new_pass = self.cleaned_data.get('new_password')
        c_new_pass =  self.cleaned_data.get('confirm_new_password')
        if new_pass != c_new_pass:
            raise forms.ValidationError('Passwords are not match !')
        return c_new_pass
    
    