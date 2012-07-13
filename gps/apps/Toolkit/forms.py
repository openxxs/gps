from django import forms

def _(msg):
    return msg

my_messages = {'required': _(u'输入不能为空')}

class transformDoyForm(forms.Form):
# TODO: Define form fields here
    dateYear = forms.CharField(required=True, error_messages=my_messages)
    dateMonth = forms.CharField(required=True, error_messages=my_messages)
    dateDay = forms.CharField(required=True, error_messages=my_messages)
    doyYear = forms.CharField(required=True, error_messages=my_messages)
    doyDay = forms.CharField(required=True, error_messages=my_messages)

	
