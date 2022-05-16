import csv
import psycopg2
import json

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

with open('countries.csv', 'rU') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		print(row)
		sqlInsert = f"""INSERT INTO public.country(
            	country, subregion, continent, northsouth)
    			VALUES (%s, %s, %s, %s);"""

		cur.execute(sqlInsert,(row[0],row[1],row[2],row[3]))
		conn.commit()