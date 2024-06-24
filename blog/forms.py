from django import forms


class PubBlogForm(forms.Form):
    title = forms.CharField(max_length=200)
    content = forms.CharField(min_length=2)
    category = forms.IntegerField()
