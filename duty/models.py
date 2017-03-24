#coding: utf-8
from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date, time, timedelta
from django.db.models import Max
import hashlib
import json

RULE_TYPE_SWAP = 1
RULE_TYPE_ADD_PEOPLE = 2
RULE_TYPE_DEL_PEOPLE = 3
RULE_TYPE_JUMP_WEEK = 4
RULE_TYPE_JUMP_DAY = 5
RULE_TYPE_SWITCH_ON = 6
RULE_TYPE_SWITCH_OFF = 7
SPLIT_SYMBLE = '|'

WEEK_NAMES = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期天' ]

def equal_date(a, b):
	return (not (a < b)) and (not (b < a))

def get_people(peoples):
	index = 0
	done_list = []
	while (peoples[index]['done'] != 0):
		done_list.append({'name':peoples[index]['name'],
			'times':peoples[index]['times'],
			'done':(peoples[index]['done'] + 1) % peoples[index]['times'],
			})
		index += 1
		if (index == len(peoples)):
			peoples = done_list
			done_list = []
			index = 0

	done_list.append({'name':peoples[index]['name'],
			'times':peoples[index]['times'],
			'done':(peoples[index]['done'] + 1) % peoples[index]['times'],
			})
	return (peoples[index]['name'], peoples[index + 1:] + done_list)






class Rule(models.Model):
	index = models.IntegerField()
	typ = models.IntegerField()
	content = models.CharField(max_length = 100)
	date = models.DateField()

	@staticmethod
	def get_all(order):
		if (order):
			raw_rules = Rule.objects.order_by('index')
		else:
			raw_rules = Rule.objects.order_by('-index')
		rules = []
		for rule in raw_rules:
			rules.append(rule.decode())
		return rules


	def decode_add_people(rule, data):
		print rule
		print data
		content = rule.content.split(SPLIT_SYMBLE)
		print content
		#print rule.content
		data['name'] = content[0]
		data['times'] = int(content[1])
		#print content[0]
		#print content[1]
		#print content[2]
		#print datetime.strptime(content[2], '%Y-%m-%d')
		data['start'] = datetime.strptime(content[2], '%Y-%m-%d')

	def decode_jump_day(rule, data):
		content = rule.content.split(SPLIT_SYMBLE)
		data['day'] = datetime.strptime(content[0], '%Y-%m-%d')

	def decode_switch(rule, data):
		content = rule.content.split(SPLIT_SYMBLE)
		data['day'] = datetime.strptime(content[0], '%Y-%m-%d')

	def decode(rule):
		data = {'index' : rule.index, 'type' : rule.typ, 'date' : rule.date}
		if (rule.typ == RULE_TYPE_ADD_PEOPLE):
			rule.decode_add_people(data)
		if (rule.typ == RULE_TYPE_JUMP_DAY):
			rule.decode_jump_day(data)
		if (rule.typ == RULE_TYPE_SWITCH_OFF):
			rule.decode_switch(data)
		return data


	@staticmethod
	def encode_add_people(data):
		return SPLIT_SYMBLE.join([data['name'], data['times'], data['start']])
	@staticmethod
	def encode_jump_day(data):
		return SPLIT_SYMBLE.join([data['day']])

	@staticmethod
	def encode(data):
		typ = int(data['type'])
		if (typ == RULE_TYPE_ADD_PEOPLE):
			return Rule.encode_add_people(data)
		if (typ == RULE_TYPE_JUMP_DAY):
			return Rule.encode_jump_day(data)


	@staticmethod
	def add_rule(data):
		index = Rule.objects.all().aggregate(Max('index'))['index__max']
		print index
		if index is None:
			index = 0
		index += 1
		new_rule = Rule(
			index = index,
			typ = data['type'],
			content = Rule.encode(data),
			date = datetime.now(),
			)
		new_rule.save()



	@staticmethod
	def get_duty():
		dutys = []
		rules = Rule.get_all(True)
		people = []
		target = datetime.strptime("2016-12-05", '%Y-%m-%d')
		now = datetime.now()
		begin = now - timedelta(5)
		end = now + timedelta(100)
		last_week = 0
		this_week = 0
		switch = RULE_TYPE_SWITCH_ON
		while target < end:
			jump = False
			for rule in rules:
				if (rule['type'] == RULE_TYPE_ADD_PEOPLE) and equal_date(target, rule['start']):
					people.append({'name' : rule['name'], 'times' : rule['times'], 'done' : 0})
				if (rule['type'] == RULE_TYPE_JUMP_DAY) and equal_date(target, rule['day']):
					jump = True
				if (rule['type'] == RULE_TYPE_SWITCH_OFF) and equal_date(target, rule['day']):
					switch = RULE_TYPE_SWITCH_OFF
			if (target.weekday() == 0):
				last_week = this_week
				this_week = 0
			if (jump):
				name = '不值班'
			elif (target.weekday() >= 5):
				name = '周末'
			elif (last_week != 0) and (switch == RULE_TYPE_SWITCH_ON):
				name = '交易'
			else:
				(name, people) = get_people(people)
				this_week += 1

			duty = {"date":target, 'name' : name}
			if (begin < target) and (target < end):
				dutys.append(duty)
			target = target + timedelta(1)
			print target
			print duty
		print dutys
		return dutys
