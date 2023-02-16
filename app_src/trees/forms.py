from django.forms import ModelForm, Select, DateTimeInput, HiddenInput

from .models import PlantedTree

class PlantedTreeForm(ModelForm):

    class Meta:
        model = PlantedTree 
        fields = ("tree", "user", "account", "planted_at")

        widgets = {
            'tree': Select(),
            'user': HiddenInput(),
            'account': Select(),
            'planted_at': DateTimeInput(),
        }
