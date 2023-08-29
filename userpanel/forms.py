from django import forms
from .models import Website, ReplacePhrase, ContentWebsite
from django.forms.widgets import TextInput


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['website_url', 'site_username', 'site_password']
        labels = {
            'website_url': 'آدرس وب‌سایت',
            'site_username': 'نام کاربری سایت',
            'site_password': 'رمز عبور سایت',
        }
        widgets = {
            'website_url': forms.TextInput(
                attrs={'placeholder': 'آدرس وب‌سایت'}),
            'site_username': forms.TextInput(
                attrs={'placeholder': 'نام کاربری سایت'}),
            'site_password': forms.PasswordInput(
                attrs={'placeholder': 'رمز عبور سایت'}),
        }


class ReplacePhraseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_sites = kwargs.pop('user_sites',
                                None)  # دریافت لیست سایت‌های کاربر
        super(ReplacePhraseForm, self).__init__(*args, **kwargs)

        if user_sites:
            self.fields[
                'website'].queryset = user_sites  # تنظیم لیست سایت‌ها برای دراپ‌دان لیست

    class Meta:
        model = ReplacePhrase
        fields = ['phrase', 'link', 'website']
        widgets = {
            'website': forms.Select(attrs={'class': 'form-control'}),
            'phrase': forms.TextInput(attrs={'placeholder': 'عبارت'}),
            'link': forms.TextInput(attrs={'placeholder': 'لینک'}),
        }


class SelectWebsiteForm(forms.Form):
    website = forms.ModelChoiceField(queryset=Website.objects.none())

    def __init__(self, user, *args, **kwargs):
        super(SelectWebsiteForm, self).__init__(*args, **kwargs)
        self.fields['website'].queryset = Website.objects.filter(user=user)


class ContentWebsiteForm(forms.ModelForm):
    class Meta:
        model = ContentWebsite
        fields = ['website', 'title', 'content', 'post_id', 'category', 'tags',
                  'publish_date', 'slug']
        widgets = {
            'website': forms.Select(attrs={'class': 'form-group'}),
            'title': forms.TextInput(attrs={'class': 'form-group'}),
            'content': forms.Textarea(attrs={'class': 'form-group'}),
            'post_id': forms.TextInput(attrs={'class': 'form-group'}),
            'category': forms.TextInput(attrs={'class': 'form-group'}),
            'tags': forms.TextInput(attrs={'class': 'form-group'}),
            'publish_date': forms.DateTimeInput(attrs={'class': 'form-group'}),
            'slug': forms.TextInput(attrs={'class': 'form-group'}),
        }


class ProcessDotsTextForm(forms.Form):
    directory_path = forms.CharField(label='ادرس سایت', max_length=500)
