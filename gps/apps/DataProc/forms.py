#!/usr/bin/env python
#coding=utf-8
from django import forms
def _(msg):
	return msg
my_messages={'required':_(u'输入不能为空')}
IGS = (
	('IGSF','IGSF'),
	('IGSR','IGSR'),
	('IGSU','IGSU'),
	)

TIMECHOICE = (
	('18:00','18:00'),
	('12:00','12:00'),
	('06:00','06:00'),
	('00:00','00:00'),
	)

class ProcessForm(forms.Form):
	StartYear = forms.CharField(label=u"开始年份",required=True,error_messages=my_messages)
	StartDay  = forms.CharField(label=u"开始天数",required=True,error_messages=my_messages)
	EndYear   = forms.CharField(label=u"结束年份",required=True,error_messages=my_messages)
	EndDay    = forms.CharField(label=u"结束天数",required=True,error_messages=my_messages)

	def clean_StartYear(self):
		StartYear = self.data.get('StartYear')
		try:
			StartYear = int(StartYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return StartYear

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

	def clean_EndDay(self):
		EndDay = self.data.get('EndDay')
		try:
			EndDay = int(EndDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return EndDay

class BulkProcessForm(ProcessForm):
    IGSParameters = forms.ChoiceField(label=u"IGS参数",required=True,choices=IGS)
    

class TrackForm(forms.Form):
	sYear  = forms.CharField(label=u"开始年份",required=True,error_messages=my_messages)
	sMonth = forms.CharField(label=u"开始月份",required=True,error_messages=my_messages)
	sDay   = forms.CharField(label=u"开始日期",required=True,error_messages=my_messages)
	sHour  = forms.CharField(label=u"开始时辰",required=True,error_messages=my_messages)
	eHour  = forms.CharField(label=u"结束时辰",required=True,error_messages=my_messages)
	sites  = forms.CharField(label=u"站点",required=True,error_messages=my_messages)
	def clean_sYear(self):
		sYear = self.data.get('sYear')
		try:
			sYear = int(sYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return sYear

	def clean_sMonth(self):
		sMonth = self.data.get('sMonth')
		try:
			sMonth = int(sMonth)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return sMonth

	def clean_sDay(self):
		sDay = self.data.get('sDay')
		try:
			sDay = int(sDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return sDay

	def clean_sHour(self):
		sHour = self.data.get('sHour')
		try:
			sHour = int(sHour)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return sHour

	def clean_eHour(self):
		eHour = self.data.get('eHour')
		try:
			eHour = int(eHour)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return eHour


class TrackRTForm(forms.Form):
	des_station   = forms.CharField(label=u"目标台站",required=True,error_messages=my_messages)
	extra_station = forms.CharField(label=u"参考台站",required=True,error_messages=my_messages)
	time          = forms.ChoiceField(label=u"sp3文件更新时间",required=True,choices=TIMECHOICE)
    