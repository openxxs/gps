#!/usr/bin/env python
#coding=utf-8
from django import forms

my_messages={'required':_(u'输入不能为空')}
IGS = (
	('IGSF','IGSF'),
	('IGSR','IGSR'),
	('IGSU','IGSU')
	)

class ProcessForm(forms.Form):
	StartYear = forms.CharField(required=True,error_messages=my_messages)
	StartDay = forms.CharField(required=True,error_messages=my_messages)
	EndYear = forms.CharField(required=True,error_messages=my_messages)
	EndDay = forms.CharField(required=True,error_messages=my_messages)

	def clean_StartYear(self):
		StartYear = self.data.get('StartYear')
		try:
			StartYear = int(StartYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))

	def clean_StartDay(self):
		StartDay = self.data.get('StartDay')
		try:
			StartDay = int(StartDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))

	def clean_EndYear(self):
		EndYear = self.data.get('EndYear')
		try:
			EndYear = int(EndYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))

	def clean_EndDay(self):
		EndDay = self.data.get('EndDay')
		try:
			EndDay = int(EndDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))

class BulkProcessForm(ProcessForm):
    IGSParameters = forms.ChoiceField(required=True,choices=IGS)
    
