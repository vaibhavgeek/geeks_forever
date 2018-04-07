import os
import pdftotext
from collections import defaultdict
# Load your PDF
from pymongo import MongoClient
import pymongo


CONNECTION = 'mongodb://abhishek:abhishek@ds143388.mlab.com:43388/intreader'
client = MongoClient(CONNECTION)
db = client.intreader


def reader():
	json = {}
	with open("Resume.pdf", "rb") as f:
		pdf = pdftotext.PDF(f)
	# mystring = pdf[3].replace('\n', ' ').replace('\r', '')
	# print(mystring.replace('\t', " ")[53:])
	
	id = 1
	db.books.insert({"id": id ,  "book_name" : "nptel" , "pages" : len(pdf)})
	previous_page = db.pages.find().sort('$natural', pymongo.DESCENDING).limit(-1).next()
	print(previous_page)
	for index,page in enumerate(pdf) :
		print("start")
		pid = previous_page["id"] + 1
		files = page.replace('\n', ' ').replace('\r', '')
		db.pages.insert({"id":pid  , "book_id" : id , "text" : files , "page_number": index })
		print("done")


reader()	