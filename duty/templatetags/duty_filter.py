#coding: utf-8
from django import template
from datetime import datetime, date, time, timedelta


register = template.Library()


@register.filter(name='mydate')
def duty_date(value):
	return {
		0:'周一',
		1:'周二',
		2:'周三',
		3:'周四',
		4:'周五',
		5:'周六',
		6:'周日',
	}[value.weekday()]
