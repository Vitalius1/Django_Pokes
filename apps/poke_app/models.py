# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count
from django.db import models
from ..log_reg.models import User

class PokeManager(models.Manager):
	def poke(self, postData):
		# print postData['poker_id'], postData['poked_id'], "*****************"
		poker = User.objects.get(id = postData['poker_id'])
		poked = User.objects.get(id = postData['poked_id'])
		self.create(poker = poker, poked = poked)
		# print self.all()
		
	def my_pokes(self, id):
		me = User.objects.get(id = id)
		all_pokes = self.filter(poked = me)
		count = all_pokes.values('poker').distinct().count()
		print count
		return count
	
	def who_poked_me(self, id):
		me = User.objects.get(id = id)
		others = []
		pokers = self.filter(poked = me).values('poker__alias').distinct()
		print pokers, "()()()()()()()()()()"
		for each in pokers:
			others.append(each)
		return others




class Poke(models.Model):
	poker=models.ForeignKey(User,related_name='user_poker',null=True)
	poked=models.ForeignKey(User,related_name='user_poked',null=True)
	created_at=models.DateField(auto_now_add=True)
	updated_at=models.DateField(auto_now=True)
	objects = PokeManager()
# Create your models here.
