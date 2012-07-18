from django import forms

def _(msg):
    return msg

class transformDoyForm(forms.Form):
# TODO: Define form fields here
	dateYear  = forms.CharField()
	dateMonth = forms.CharField()
	dateDay   = forms.CharField()
	doyYear   = forms.CharField()
	doyDay    = forms.CharField()

	def clean_dateYear(self):
		dateYear = self.data.get('dateYear')
		try:
			dateYear = int(dateYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return dateYear

	def clean_dateMonth(self):
		dateMonth = self.data.get('dateMonth')
		try:
			dateMonth = int(dateMonth)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return dateMonth

	def clean_dateDay(self):
		dateDay = self.data.get('dateDay')
		try:
			dateDay = int(dateDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return dateDay

	def clean_doyYear(self):
		doyYear = self.data.get('doyYear')
		try:
			doyYear = int(doyYear)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return doyYear

	def clean_doyDay(self):
		doyDay = self.data.get('doyDay')
		try:
			doyDay = int(doyDay)
		except:
			raise forms.ValidationError(_('输入的日期格式不正确'))
		return doyDay
