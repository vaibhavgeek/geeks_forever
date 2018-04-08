# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.conf import settings

import os
import pdftotext
from collections import defaultdict
# Load your PDF
from pymongo import MongoClient
import pymongo
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from app.models import Uploads
from app.forms import UploadForm
import PyPDF2
import requests
from django.views.decorators.csrf import csrf_exempt

import json

CONNECTION = 'mongodb://abhishek:abhishek@ds239029.mlab.com:39029/intreader'
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
			previous_book = {"id" : 0}

		previous_book1 = previous_book["id"] + 1

		#storing the file in a fold

		form = UploadForm(request.POST, request.FILES)
		print("outsite")
		if form.is_valid():
			print("done")
			newdoc = Uploads(file = request.FILES['file'] , bookid = previous_book1 , filename = request.FILES['file'].name)
			newdoc.save()
		else:
			return render(request,'home.html', {'form': form})

		db.books.insert({"id": previous_book1 ,  "book_name" : "nptel" , "pages" : len(pdf)})
		try:
			previous_page = db.pages.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
		except :
			previous_page = { "id": 0}
		
		pid = previous_page["id"]
		for index,page in enumerate(pdf) :
			
			pid +=  1
			files = page.replace('\n', ' ').replace('\r', '')
			db.pages.insert({"id":pid  , "book_id" : previous_book1 , "text" : files , "page_number": index })

		return redirect('questions', book_id=previous_book1)

	form = UploadForm()
	return render(request,'home.html', {'form':form})


def questions(request,book_id):

	uploads  = Uploads.objects.get(bookid = book_id)
	file_path = settings.MEDIA_ROOT +'/'+ "uploads/"+ book_id+ "/" +uploads.filename
	print(file_path)
	return render(request, "questions.html" ,{ 'book_id' :book_id})



def download(request,book_id):
	uploads  = Uploads.objects.get(bookid = book_id)
	file_path = settings.MEDIA_ROOT +'/'+ "uploads/"+ book_id+ "/" +uploads.filename
	print(file_path)
	
	
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/pdf")
			response['Content-Disposition'] = 'inline; filename=' + uploads.filename
			return response


def page(request,book_id,page_no):
	uploads  = Uploads.objects.get(bookid = book_id)
	file_path = settings.MEDIA_ROOT +'/'+ "uploads/"+ book_id+ "/" +uploads.filename
	print(file_path)
	v = open(file_path, 'r')
	fh = PyPDF2.PdfFileReader(v)		
	pdf = fh.getPage(int(page_no))
	pdfWriter = PyPDF2.PdfFileWriter()
	pdfWriter.addPage(pdf)
	
	#rough



	
	file_path2 = settings.MEDIA_ROOT +'/'+ "uploads/test.pdf"
	if os.path.exists(file_path):
		with open(file_path2, "wb") as outputStream:
			pdfWriter.write(outputStream)
		with open(file_path2, "rb") as data:
			response = HttpResponse(data.read(), content_type="application/pdf")
			response['Content-Disposition'] = 'inline; filename=' + uploads.filename
			v.close()
			return response


@csrf_exempt
def query(request):
	request1 = request.body
	question = json.loads(request1.decode("utf-8"))["question"]
	print(question)
	bookid = json.loads(request1.decode("utf-8"))["book_id"]
	
	print(bookid)

	url = "http://35.196.112.1/"
	payload = '{"question":"' + question +'" , "book_id":"' + str(12) + '"}'
	headers = {
	'content-type': "application/json",
	'cache-control': "no-cache",
	'postman-token': "841456cb-b4ff-95cb-7ad6-dab7956dea76"
	}
	response = requests.request("POST", url, data=payload, headers=headers)
	print(response)
	return HttpResponse(response)
