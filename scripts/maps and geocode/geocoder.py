import googlemaps
from datetime import datetime
import psycopg2
import json

gmaps = googlemaps.Client(key='insert api key')

# Geocoding an address

#connect to do database
with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

sqlInst = """SELECT * from institute
where institute.lat is null and institute_name is not null and score>0.1
order by score desc"""

cur.execute(sqlInst)
sqlInstRows = cur.fetchall()
for row in sqlInstRows:
	if row[1]!= '':
		print(row[1])

		geocode_result = gmaps.geocode(row[1].strip())
		if len(geocode_result)>0:
			for comp in geocode_result[0]['address_components']:
				if len(comp['types'])>0:
					if comp['types'][0]=='country':
						country = comp['long_name']

			lat = geocode_result[0]['geometry']['location']['lat']
			lon = geocode_result[0]['geometry']['location']['lng']
			print(country)
			sqlUpdate = f"""UPDATE public.institute
				   	SET country_str=%s, lat={lat}, lon={lon}
				 	WHERE institute_id={row[0]};"""

			cur.execute(sqlUpdate,(country,))
			conn.commit()

conn.close()