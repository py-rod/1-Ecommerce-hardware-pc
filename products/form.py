from django import forms
from .models import ReviewProduct


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewProduct
        fields = ["review", "rating"]
        widgets = {
            "review": forms.Textarea(attrs={"required": True, "class": "write-review", "placeholder": "Escribe tu comentario"})
        }
