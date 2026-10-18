from django import forms

from .models import Lead, Service


class LeadForm(forms.ModelForm):
    # Honeypot: real people never see or fill this field.
    nickname = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "company", "website", "service", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@company.com"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "placeholder": "+91 …", "inputmode": "tel"}),
            "company": forms.TextInput(attrs={"autocomplete": "organization", "placeholder": "Business name"}),
            "website": forms.TextInput(attrs={"placeholder": "yourbusiness.com (if you have one)"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "What would you like to build or improve?"}),
        }
        labels = {"phone": "Phone / WhatsApp", "company": "Business", "website": "Current website",
                  "service": "What do you need?", "message": "Tell us about the project"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(is_published=True)
        self.fields["service"].empty_label = "Not sure yet"
        self.fields["nickname"].label = "Leave this empty"

    def clean_nickname(self):
        if self.cleaned_data.get("nickname"):
            raise forms.ValidationError("Spam detected.")
        return ""
