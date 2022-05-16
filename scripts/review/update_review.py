import csv
import psycopg2
import json

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

with open('review_sets.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		print(row)

		sqlUpdate = f"""UPDATE public.paper
			SET reviewed='{row[2]}'
			WHERE paper_id={row[0]}"""
		print(sqlUpdate)
		cur.execute(sqlUpdate)
		conn.commit()