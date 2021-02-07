from django import forms
from .models import Replies

class RepliesForm(forms.ModelForm):

	content = forms.CharField(widget = forms.Textarea(attrs ={
		'class':'form-control',
		'placeholder':'',
		'id':"usercomment",
		'rows':4
		}))
	class Meta:
		model= Replies
		fields = ['content',]