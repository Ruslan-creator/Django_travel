from django import forms

from authapp.forms import TravelUserEditForm
from authapp.models import TravelUser
from mainapp.models import Accommodation, ListOfCountries
from comment.models import Comment

# Форма редактирования параметров пользователя
class TravelUserAdminEditForm(TravelUserEditForm):
    class Meta:
        model = TravelUser
        fields = "__all__"


# Форма редактирования параметров стран
class ListOfCountriesEditForm(forms.ModelForm):
    class Meta:
        model = ListOfCountries
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""


# Форма редактирования параметров услуг компании
class AccommodationEditForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs["class"] = "form-control"
                field.help_text = ""

# Форма редактирования комментариев
class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs["class"] = "form-control"
                field.help_text = ""
