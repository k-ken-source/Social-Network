from django import forms
from .models import post, Comment, blog
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
	def use_required_attribute(self,*args):
		return False

class PostForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCEWidget(
	 		attrs={'required': False, 'cols': 30, 'rows': 10}
	 	))

	class Meta:
		model = post
		fields= ['title','overview','thumbnail','content']

class BlogForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCEWidget(
	 		attrs={'required': False, 'cols': 30, 'rows': 10}
	 	))

	class Meta:
		model = blog
		fields= ['title','content']

class CommentForm(forms.ModelForm):
	content = forms.CharField(widget = forms.Textarea(attrs ={
		'class':'form-control',
		'placeholder':'Type your comment',
		'id':"usercomment",
		'rows':4
		}))
	class Meta:
		model= Comment
		fields = ['content',]


