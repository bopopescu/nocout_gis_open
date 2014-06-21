from django import forms
from models import Antenna

# antenna form
class AntennaForm(forms.ModelForm):

    POLARIZATION = (
        ('', 'Select....'),
        ('vertical', 'Vertical'),
        ('horizontal', 'Horizontal')
    )

    SPLITTER_INSTALLED = (
        ('', 'Select....'),
        ('yes', 'Yes'),
        ('no', 'No')
    )

    polarization = forms.TypedChoiceField(choices=POLARIZATION, required=False)
    splitter_installed = forms.TypedChoiceField(choices=SPLITTER_INSTALLED, required=False)
    sync_splitter_used = forms.TypedChoiceField(choices=SPLITTER_INSTALLED, required=False)

    def __init__(self, *args, **kwargs):
        super(AntennaForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})
    class Meta:
        model = Antenna
