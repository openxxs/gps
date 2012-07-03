#!/usr/bin/env python
#coding=utf-8
from django import forms

my_messages={'required':_(u'输入不能为空')}
IGS = (
	('IGSF','IGSF')
	('IGSR','IGSR'),
	()
	)

class ProcessForm(forms.Form):
	StartYear = forms.CharField(required=True,error_messages=my_messages)
	StartDay = forms.CharField(required=True,error_messages=my_messages)
	EndYear = forms.CharField(required=True,error_messages=my_messages)
	EndDay = forms.CharField(required=True,error_messages=my_messages)

class BulkProcessForm(ProcessForm):
    IGSParameters = forms.ChoiceField(required=True,choices=IGS)
    
