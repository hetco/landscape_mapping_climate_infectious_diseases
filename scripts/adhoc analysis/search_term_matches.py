import json
import psycopg2

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

searchList2 = [
['Vector Borne Diseases ','"vector borne diseases"[MeSH Terms] OR ("vector"[All Fields] AND "borne"[All Fields] AND "diseases"[All Fields]) OR "vector borne diseases"[All Fields]'],
['Dengue','"dengue"[MeSH Terms] OR "dengue"[All Fields] OR "dengue\'s"[All Fields]'],
['Malaria','"malaria"[MeSH Terms] OR "malaria"[All Fields] OR "malarias"[All Fields] OR "malaria\'s"[All Fields] OR "malariae"[All Fields]'],
['Zika','"zika virus"[MeSH Terms] OR ("zika"[All Fields] AND "virus"[All Fields]) OR "zika virus"[All Fields] OR "zika"[All Fields] OR "zika virus infection"[MeSH Terms] OR ("zika"[All Fields] AND "virus"[All Fields] AND "infection"[All Fields]) OR "zika virus infection"[All Fields]'],
['Chikugunya','"chikungunya fever"[MeSH Terms] OR ("chikungunya"[All Fields] AND "fever"[All Fields]) OR "chikungunya fever"[All Fields] OR "chikungunya"[All Fields]'],
['Leprospirosis','"leptospirosis"[MeSH Terms] OR "leptospirosis"[All Fields] OR "leptospiroses"[All Fields]'],
['Cholera','"cholera"[MeSH Terms] OR "cholera"[All Fields] OR "choleras"[All Fields] OR "cholera\'s"[All Fields] OR "cholerae"[All Fields] OR "cholerae\'s"[All Fields] OR "choleraic"[All Fields]'],
['Rift Valley/ Rift Valley Fever','rift valley fever"[MeSH Terms] OR ("rift"[All Fields] AND "valley"[All Fields] AND "fever"[All Fields]) OR "rift valley fever"[All Fields]'],
['Plague','"plague"[MeSH Terms] OR "plague"[All Fields] OR "plagues"[All Fields]'],
['Diarrhea','"diarrhea"[MeSH Terms] OR "diarrhea"[All Fields] OR "diarrheas"[All Fields] OR "diarrhoea"[All Fields] OR "diarrhoeas"[All Fields]'],
['Hantavirus Pulmonary Syndrome','"hantavirus pulmonary syndrome"[MeSH Terms] OR ("hantavirus"[All Fields] AND "pulmonary"[All Fields] AND "syndrome"[All Fields]) OR "hantavirus pulmonary syndrome"[All Fields]'],
['Hemorrhagic Fever with Renal Syndrome','"haemorrhagic fever with renal syndrome"[All Fields] OR "hemorrhagic fever with renal syndrome"[MeSH Terms] OR ("hemorrhagic"[All Fields] AND "fever"[All Fields] AND "renal"[All Fields] AND "syndrome"[All Fields]) OR "hemorrhagic fever with renal syndrome"[All Fields]'],
['Respiratory Syncitial Virus (RSV)','"respiratory syncytial viruses"[MeSH Terms] OR ("respiratory"[All Fields] AND "syncytial"[All Fields] AND "viruses"[All Fields]) OR "respiratory syncytial viruses"[All Fields] OR ("respiratory"[All Fields] AND "syncytial"[All Fields] AND "virus"[All Fields] AND "rsv"[All Fields]) OR "respiratory syncytial virus rsv"[All Fields]'],
['Influenza','"influenza\'s"[All Fields] OR "influenza, human"[MeSH Terms] OR ("influenza"[All Fields] AND "human"[All Fields]) OR "human influenza"[All Fields] OR "influenza"[All Fields] OR "influenzae"[All Fields] OR "influenzas"[All Fields]'],
['Vibrio ','"vibrio"[MeSH Terms] OR "vibrio"[All Fields] OR "vibrios"[All Fields]'],
['Ebola','"ebola\'s"[All Fields] OR "hemorrhagic fever, ebola"[MeSH Terms] OR ("hemorrhagic"[All Fields] AND "fever"[All Fields] AND "ebola"[All Fields]) OR "ebola hemorrhagic fever"[All Fields] OR "ebola"[All Fields] OR "ebolavirus"[MeSH Terms] OR "ebolavirus"[All Fields]'],
['Schistosomiasis','"schistosomiasis"[MeSH Terms] OR "schistosomiasis"[All Fields] OR "schistosomiases"[All Fields]'],
['Tick borne disease','"tick-borne diseases"[MeSH Terms] OR ("tick-borne"[All Fields] AND "diseases"[All Fields]) OR "tick-borne diseases"[All Fields] OR ("tick"[All Fields] AND "borne"[All Fields] AND "disease"[All Fields]) OR "tick borne disease"[All Fields]'],
['Chagas','"chaga"[All Fields] OR "chaga\'s"[All Fields] OR "chagas"[All Fields] OR "chagas\'s"[All Fields]'],
['Filariasis','"filariasis"[MeSH Terms] OR "filariasis"[All Fields] OR "filariases"[All Fields]'],
['Trypanosomiasis (tsetse flies - Glossina sp)','"trypanosomiasis"[MeSH Terms] OR "trypanosomiasis"[All Fields] OR "trypanosomiases"[All Fields]'],
['Yellow fever','"yellow fever"[MeSH Terms] OR ("yellow"[All Fields] AND "fever"[All Fields]) OR "yellow fever"[All Fields]'],
['Aedes','"aedes"[MeSH Terms] OR "aedes"[All Fields]'],
['Anopheles','"anophele"[All Fields] OR "anopheles"[MeSH Terms] OR "anopheles"[All Fields]'],
['Culex','"culex"[MeSH Terms] OR "culex"[All Fields]'],
['Leishmaniasis','"leishmaniasis"[MeSH Terms] OR "leishmaniasis"[All Fields] OR "leishmaniases"[All Fields] OR "leishmaniasis vaccines"[MeSH Terms] OR ("leishmaniasis"[All Fields] AND "vaccines"[All Fields]) OR "leishmaniasis vaccines"[All Fields]'],
['Salmonellosis','"salmonella infections"[MeSH Terms] OR ("salmonella"[All Fields] AND "infections"[All Fields]) OR "salmonella infections"[All Fields] OR "salmonellosis"[All Fields] OR "salmonella food poisoning"[MeSH Terms] OR ("salmonella"[All Fields] AND "food"[All Fields] AND "poisoning"[All Fields]) OR "salmonella food poisoning"[All Fields]'],
['Giardiasis','"giardiasis"[MeSH Terms] OR "giardiasis"[All Fields] OR "giardiases"[All Fields]'],
['new and emerging infectious diseases','"communicable diseases, emerging"[MeSH Terms] OR ("communicable"[All Fields] AND "diseases"[All Fields] AND "emerging"[All Fields]) OR "emerging communicable diseases"[All Fields] OR ("emerging"[All Fields] AND "infectious"[All Fields] AND "diseases"[All Fields]) OR "emerging infectious diseases"[All Fields]'],
['climate-sensitive infectious diseases','"communicable diseases"[MeSH Terms] OR ("communicable"[All Fields] AND "diseases"[All Fields]) OR "communicable diseases"[All Fields] OR ("infectious"[All Fields] AND "diseases"[All Fields]) OR "infectious diseases"[All Fields]'],
['allergic disease','"allergic"[All Fields] OR "allergical"[All Fields] OR "allergically"[All Fields] OR "allergics"[All Fields] OR "allergization"[All Fields] OR "allergizing"[All Fields]'],
['Onchocercosis','"onchocerciasis"[MeSH Terms] OR "onchocerciasis"[All Fields] OR "onchocercosis"[All Fields]'],
['babesiosis','"babesiosis"[MeSH Terms] OR "babesiosis"[All Fields] OR "babesioses"[All Fields]'],
['rabies','"rabies"[MeSH Terms] OR "rabies"[All Fields'],
['anaplasmosis','"anaplasmosis"[MeSH Terms] OR "anaplasmosis"[All Fields] OR "anaplasmoses"[All Fields]'],
['Campylobacter infection','"campylobacter infections"[MeSH Terms] OR ("campylobacter"[All Fields] AND "infections"[All Fields]) OR "campylobacter infections"[All Fields] OR ("campylobacter"[All Fields] AND "infection"[All Fields]) OR "campylobacter infection"[All Fields]'],
['Borreliosis','"borrelia infections"[MeSH Terms] OR ("borrelia"[All Fields] AND "infections"[All Fields]) OR "borrelia infections"[All Fields] OR "borreliosis"[All Fields]'],
['West Nile Fever','"west nile fever"[MeSH Terms] OR ("west"[All Fields] AND "nile"[All Fields] AND "fever"[All Fields]) OR "west nile fever"[All Fields]'],
['Botulism','"botulism"[MeSH Terms] OR "botulism"[All Fields]'],
['Anthrax','"anthrax"[MeSH Terms] OR "anthrax"[All Fields]'],
['Clostridiosis','"clostridium infections"[MeSH Terms] OR ("clostridium"[All Fields] AND "infections"[All Fields]) OR "clostridium infections"[All Fields] OR "clostridiosis"[All Fields]'],
['Pasteurellosis','"pasteurella infections"[MeSH Terms] OR ("pasteurella"[All Fields] AND "infections"[All Fields]) OR "pasteurella infections"[All Fields] OR "pasteurellosis"[All Fields]'],
['Parapoxvirus','"parapoxvirus"[MeSH Terms] OR "parapoxvirus"[All Fields] OR "parapoxviruses"[All Fields]'],
['Pestivirus','"pestivirus"[MeSH Terms] OR "pestivirus"[All Fields] OR "pestiviruses"[All Fields]'],
['Necrobacillosis','"fusobacterium infections"[MeSH Terms] OR ("fusobacterium"[All Fields] AND "infections"[All Fields]) OR "fusobacterium infections"[All Fields] OR "necrobacillosis"[All Fields]'],
['Alphaherpes virus','"alphaherpesvirus"[All Fields]'],
['Gammaherpes virus','"gammaherpesvirus"[All Fields]'],
['Clostridiosis','"clostridium infections"[MeSH Terms] OR ("clostridium"[All Fields] AND "infections"[All Fields]) OR "clostridium infections"[All Fields] OR "clostridiosis"[All Fields]'],
['Cryptosporidiosis','"cryptosporidiosis"[MeSH Terms] OR "cryptosporidiosis"[All Fields] OR "cryptosporidioses"[All Fields]'],
['drug-resistant infections','"drug resistance"[MeSH Terms] OR ("drug"[All Fields] AND "resistance"[All Fields]) OR "drug resistance"[All Fields] OR ("drug"[All Fields] AND "resistant"[All Fields]) OR "drug resistant"[All Fields]'],
['epidemic','"epidemic\'s"[All Fields] OR "epidemical"[All Fields] OR "epidemically"[All Fields] OR "epidemicity"[All Fields] OR "epidemics"[MeSH Terms] OR "epidemics"[All Fields] OR "epidemic"[All Fields] OR "epidemiology"[Subheading] OR "epidemiology"[All Fields]'],
['pandemic','"pandemic\'s"[All Fields] OR "pandemically"[All Fields] OR "pandemicity"[All Fields] OR "pandemics"[MeSH Terms] OR "pandemics"[All Fields] OR "pandemic"[All Fields]'],
['disease-escalation','"disease-escalation"[All Fields]'],
['Tuberculosis','"tuberculosi"[All Fields] OR "tuberculosis"[MeSH Terms] OR "tuberculosis"[All Fields] OR "tuberculoses"[All Fields] OR "tuberculosis\'s"[All Fields]'],
['neglected tropical diseases','("neglect"[All Fields] OR "neglected"[All Fields] OR "neglectful"[All Fields] OR "neglecting"[All Fields] OR "neglects"[All Fields]) AND ("tropic"[All Fields] OR "tropical"[All Fields] OR "tropicalization"[All Fields] OR "tropically"[All Fields] OR "tropics"[All Fields]) AND ("disease"[MeSH Terms] OR "disease"[All Fields] OR "diseases"[All Fields] OR "disease s"[All Fields] OR "diseased"[All Fields])'],
]

for searchTerm in searchList2:
	lowerSearch = searchTerm[0].lower()

	sqlSearch = f"""select sum(papers_found) from searches
		where lower(search_terms) like '%{lowerSearch}%'"""

	cur.execute(sqlSearch)
	sqlSearchCount = cur.fetchall()[0][0]
	print(lowerSearch +'|'+str(sqlSearchCount))




