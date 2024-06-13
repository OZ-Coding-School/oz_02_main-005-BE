from django import forms
from dateset.models import Rate

class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['rate']
        
        widgets = {
            'rate': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        labels = {
            'rate': 'Rating (1 to 5)',
        }

    def clean_rate(self):
        rate = self.cleaned_data.get('rate')
        if rate < 1 or rate > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rate
