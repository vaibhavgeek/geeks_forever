# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

import os
import pdftotext
from collections import defaultdict
# Load your PDF
from pymongo import MongoClient
import pymongo
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

CONNECTION = 'mongodb://abhishek:abhishek@ds143388.mlab.com:43388/intreader'
client = MongoClient(CONNECTION)
db = client.intreader


def reader(request):
	if request.method == "POST":
		json = {}
		file = request.FILES['file']
		pdf = pdftotext.PDF(file)
		# mystring = pdf[3].replace('\n', ' ').replace('\r', '')
		# print(mystring.replace('\t', " ")[53:])
		
		try:
			previous_book = db.books.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
		
		except:
			previous_book = {"id" : 1}

		previous_book1 = previous_book["id"] + 1

		db.books.insert({"id": previous_book1 ,  "book_name" : "nptel" , "pages" : len(pdf)})

		try:
			previous_page = db.pages.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
		except :
			previous_page = { "id": 0}
		
		pid = previous_page["id"]
		print(previous_page)

		for index,page in enumerate(pdf) :
			
			pid +=  1

			print(page)
			files = page.replace('\n', ' ').replace('\r', '')
			db.pages.insert({"id":pid  , "book_id" : previous_book1 , "text" : files , "page_number": index })

		return redirect('questions', book_id=previous_book1)
		
		return render()

	return render(request,'home.html')


def questions(request,book_id):


	return render(request, "questions.html")
