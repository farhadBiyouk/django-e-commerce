from django import forms
from home.models import Comment


class CommentProductForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'rate')


class ReplyCommentProductForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)
