from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ShareByEmailForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class PostForm(forms.ModelForm):

    # add html to your form fields  
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'markdown-content'
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_method = 'post'
        # self.helper.form_action = 'submit_survey'
        # self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Post
        fields = ['title', 'tags', 'content']
        widgets = {
            'content': PagedownWidget()
        }
