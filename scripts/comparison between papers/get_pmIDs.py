#libraries
import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import json
import time
import csv

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

start = 0
#with open('lookup_15900.json') as f:
#  output = json.load(f)
output = []

with open('Machine_learning_papers.csv') as csv_file:
	
	csv_reader = csv.reader(csv_file, delimiter=',')
	i=0
	for row in csv_reader:
		if i>start:
			#encode parameters
			params = {"tool":"tool_landscape_mapping","email":"simon@hetco.io","ids":row[3]}
			paramsEncode = urllib.parse.urlencode(params)
			print(i)
			#create URL
			url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?{paramsEncode}"
			print(url)
			#request content
			try:
				contents = urllib.request.urlopen(url).read()
				#extract PMIDs from results
				soup = BeautifulSoup(contents,'html.parser')
				pmid = soup.record['pmid']
				print(pmid)
			except:
				pmid = "No ID"
				print('Not found')

			output.append([row[3],pmid])
			time.sleep(0.05)
			
			if i % 100 == 0:
				with open('lookup_'+str(i)+'.json', 'w') as outfile:
					json.dump(output, outfile)
		i=i+1
print(output)

with open('lookup.json', 'w') as outfile:
    json.dump(output, outfile)

cur.close()
