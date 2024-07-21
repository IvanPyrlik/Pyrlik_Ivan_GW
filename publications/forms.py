from django import forms
from publications.models import Publication


class PublicationForm(forms.ModelForm):
    """Форма публикации"""
    class Meta:
        model = Publication
        fields = ['name', 'content', 'image', 'is_active', 'paid_publication']

    def __init__(self, user, *args, **kwargs, ):
        self.user = user
        super(PublicationForm, self).__init__(*args, **kwargs)

        if not self.user.activ_subscription:
            del self.fields['paid_publication']

        for field_name, field in self.fields.items():
            if field_name != 'paid_publication' and field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control'
