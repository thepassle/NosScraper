import time
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup

def databaseGetOne(query):
	conn= pymysql.connect(host='www52.totaalholding.nl',user='thepas1q_pascal',password='karel',db='thepas1q_test_base',charset='utf8mb4')
	sql=str(query)
	a=conn.cursor()
	a.execute(sql)
	data = a.fetchone()
	a.close()
	return data

def databaseGetAll(query):
	conn= pymysql.connect(host='www52.totaalholding.nl',user='thepas1q_pascal',password='karel',db='thepas1q_test_base',charset='utf8mb4')
	sql=str(query)
	a=conn.cursor()
	a.execute(sql)
	data = a.fetchall()
	a.close()
	return data

def databaseDo(query):
	conn= pymysql.connect(host='www52.totaalholding.nl',user='thepas1q_pascal',password='karel',db='thepas1q_test_base',charset='utf8mb4')
	sql=str(query)
	a=conn.cursor()
	a.execute(sql)
	a.close()

def find_news(link):

	page = urlopen(link)
	soep = BeautifulSoup(page.read(), "html.parser")
	hits = soep.findAll('div',attrs={'class':'list-items__content'})

	oldheadlines = databaseGetAll("SELECT headline FROM freeknos")

	for hit in hits:

		newheadline = str(hit.findAll('h3',attrs={'class':'list-items__title link-hover'})[0].contents[0].replace("'",""))
		tijd = str(hit.findAll('time')[0].contents[0].strip())

		if not oldheadlines:
			databaseDo("INSERT INTO freeknos (headline, tijd) VALUES ('"+str(newheadline)+"', '"+str(tijd)+"') ")
		else:
			headlineExists = False
			for oldheadline in oldheadlines:
				if oldheadline[0] in newheadline:
					headlineExists = True
					break
				else:
					pass
			if headlineExists == False:
				print("New headline added: "+str(newheadline))
				databaseDo("INSERT INTO freeknos (headline, tijd) VALUES ('"+str(newheadline)+"', '"+str(tijd)+"') ")

if __name__ == "__main__":
	iteration = 0
	while True:
		iteration+=1
		print("Iteration: "+str(iteration))
		try:
			find_news("http://nos.nl/nieuws/buitenland/")
		except:
			print("There was an error!")
		time.sleep(60)

