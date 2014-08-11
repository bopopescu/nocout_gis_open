from django import forms
from user_profile.models import UserProfile
from nocout.widgets import MultipleToSingleSelectionWidget


class UserForm(forms.ModelForm):
    """
    Class Based User Form required to create, update and update my profile of the user.
    """

    first_name = forms.CharField(required=True)
    email = forms.CharField(label='Email', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request', None)
        initial = kwargs.setdefault('initial',{})

        # removing help text for username 'select' field
        self.base_fields['username'].help_text = ''

        # removing help text for role 'select' field
        self.base_fields['role'].help_text = ''

        if kwargs['instance']:
            initial['role'] = kwargs['instance'].role.values_list('pk', flat=True)[0]
            initial['parent'] = kwargs['instance'].parent
            initial['organization'] = kwargs['instance'].organization

        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['parent'].empty_label = 'Select'
        self.fields['organization'].empty_label = 'Select'

        if self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            if self.instance.pk == self.request.pk:
                self.fields['username'].widget.attrs['readonly'] = True
                self.fields['parent'].widget.attrs['disabled'] = 'disabled'
                self.fields['role'].widget.attrs['disabled'] = 'disabled'
                self.fields['organization'].widget.attrs['readonly'] = True
                self.fields['parent'].label='Manager'
                self.fields.pop('comment')

        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                if isinstance(field.widget, forms.widgets.Select):
                    field.widget.attrs['class'] += ' col-md-12'
                    field.widget.attrs['class'] += ' select2select'
                else:
                    field.widget.attrs['class'] += ' form-control'
            else:
                if isinstance(field.widget, forms.widgets.Select):
                    field.widget.attrs.update({'class': 'col-md-12 select2select'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        """
        Meta Information required to generate model form, and to mention the fields, widgets and fieldsets
        information required to render for the form.
        """
        model = UserProfile
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 'parent', 'designation', 'company',
            'address', 'phone_number', 'comment','organization'
        )
        widgets = {
            'role': MultipleToSingleSelectionWidget,
        }
        fieldsets = (
            ('Personal', {
                'fields': ('first_name', 'last_name')
            }),
        )

    def clean_password2(self):
        # Check that the two password entries match
        password2 = self.cleaned_data.get("password2")
        password1 = self.cleaned_data.get("password1")
        if (password1 or password2) and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
