#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#创建类
import time, uuid
from orm_panjueshu import Model, StringField, TextField, LongtextField,IntField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class panjueshu(Model):
	__table__ = 'panjueshu'
	#id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
	id=IntField(primary_key=True,ddl='int(10)')
	name = StringField(ddl='varchar(200)')
	cause = StringField(ddl='varchar(200)')
	docid = StringField(ddl='varchar(100)')
	area = StringField(ddl='varchar(200)')
	proced = StringField(ddl='varchar(200)')
	types = StringField(ddl='varchar(50)')
	num = StringField(ddl='varchar(100)')
	court = StringField(ddl='varchar(100)')
	dates = StringField(ddl='varchar(200)')
	yiju=TextField()
	content=LongtextField()
	url = StringField(ddl='varchar(100)')
