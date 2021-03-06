#!/usr/bin/env python
#coding=utf-8
from django import forms

def _(msg):
	return msg
my_messages={'required':_(u'输入不能为空')}

class ViewForm(forms.Form):
	StartYear  = forms.CharField(required=True,error_messages=my_messages)
	StartMonth = forms.CharField(required=True,error_messages=my_messages)
	StartDay   = forms.CharField(required=True,error_messages=my_messages)
	EndYear    = forms.CharField(required=True,error_messages=my_messages)
	EndMonth   = forms.CharField(required=True,error_messages=my_messages)
	EndDay     = forms.CharField(required=True,error_messages=my_messages)
	Trend      = forms.CharField(required=True,error_messages=my_messages)

	def clean_StartYear(self):
		StartYear = self.data.get('StartYear')
		try:
			StartYear = int(StartYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return StartYear

	def clean_StartMonth(self):
		StartMonth = self.data.get('StartMonth')
		try:
			StartMonth = int(StartMonth)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return StartMonth

	def clean_StartDay(self):
		StartDay = self.data.get('StartDay')
		try:
			StartDay = int(StartDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return StartDay

	def clean_EndYear(self):
		EndYear = self.data.get('EndYear')
		try:
			EndYear = int(EndYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return EndYear

	def clean_EndMonth(self):
		EndMonth = self.data.get('EndMonth')
		try:
			EndMonth = int(EndMonth)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return EndMonth

	def clean_EndDay(self):
		EndDay = self.data.get('EndDay')
		try:
			EndDay = int(EndDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return EndDay
    
