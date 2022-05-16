#libraries
import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import json
import time

#######################
#user defined variables
#######################

searchList1 = [
['Climate ','"climate"[MeSH Terms] OR "climate"[All Fields] OR "climates"[All Fields] OR "climate\'s"[All Fields] OR "climatic"[All Fields] OR "climatically"[All Fields]'],
['Seasonal ','"season\'s"[All Fields] OR "seasonability"[All Fields] OR "seasonable"[All Fields] OR "seasonably"[All Fields] OR "seasonal"[All Fields] OR "seasonalities"[All Fields] OR "seasonality"[All Fields] OR "seasonally"[All Fields] OR "seasonals"[All Fields] OR "seasons"[MeSH Terms] OR "seasons"[All Fields] OR "season"[All Fields]'],
['Subseasonal ','"Subseasonal"[All Fields]'],
['Hydrometeorolgical','"hydro-meteorological"[All Fields]'],
['Meteorological','"meteorologic"[All Fields] OR "meteorological"[All Fields] OR "meteorologically"[All Fields]'],
['Precipitation','"precipitability"[All Fields] OR "precipitable"[All Fields] OR "precipitant"[All Fields] OR "precipitants"[All Fields] OR "precipitate"[All Fields] OR "precipitated"[All Fields] OR "precipitates"[All Fields] OR "precipitating"[All Fields] OR "precipitation"[All Fields] OR "precipitations"[All Fields] OR "precipitative"[All Fields]'],
['Rainfall','"rainfall"[All Fields] OR "rainfalls"[All Fields]'],
['Drought','"droughted"[All Fields] OR "droughting"[All Fields] OR "droughts"[MeSH Terms] OR "droughts"[All Fields] OR "drought"[All Fields]'],
['Wind','"wind"[MeSH Terms] OR "wind"[All Fields]'],
['Temperature','"temperature"[MeSH Terms] OR "temperature"[All Fields] OR "temperatures"[All Fields] OR "temperature\'s"[All Fields]'],
['Diurnal','"diurnal"[All Fields] OR "diurnality"[All Fields] OR "diurnally"[All Fields]'],
['Humidity','"humid"[All Fields] OR "humidity"[MeSH Terms] OR "humidity"[All Fields] OR "humidities"[All Fields]'],
['Warming','"warmed"[All Fields] OR "warming"[All Fields] OR "warming\'s"[All Fields] OR "warmings"[All Fields] OR "warms"[All Fields]'],
['Global Warming','"global warming"[MeSH Terms] OR ("global"[All Fields] AND "warming"[All Fields]) OR "global warming"[All Fields] OR ("warming"[All Fields] AND "global"[All Fields]) OR "warming, global"[All Fields]'],
['Flooding','"floodings"[All Fields] OR "floods"[MeSH Terms] OR "floods"[All Fields] OR "flood"[All Fields] OR "flooded"[All Fields] OR "implosive therapy"[MeSH Terms] OR ("implosive"[All Fields] AND "therapy"[All Fields]) OR "implosive therapy"[All Fields] OR "flooding"[All Fields]'],
['extreme weather','"extreme weather"[MeSH Terms] OR ("extreme"[All Fields] AND "weather"[All Fields]) OR "extreme weather"[All Fields]'],
['wildfires','"wildfires"[MeSH Terms] OR "wildfires"[All Fields] OR "wildfire"[All Fields]'],
['climate sensitivity','("climate"[MeSH Terms] OR "climate"[All Fields] OR "climates"[All Fields] OR "climate s"[All Fields] OR "climatic"[All Fields] OR "climatically"[All Fields]) AND ("hypersensitivity"[MeSH Terms] OR "hypersensitivity"[All Fields] OR "sensitive"[All Fields] OR "sensitively"[All Fields] OR "sensitives"[All Fields] OR "sensitivities"[All Fields] OR "sensitivity and specificity"[MeSH Terms] OR ("sensitivity"[All Fields] AND "specificity"[All Fields]) OR "sensitivity and specificity"[All Fields] OR "sensitivity"[All Fields])'],
['storms','"storm"[All Fields] OR "storm\'s"[All Fields] OR "storms"[All Fields]'],
['thunderstorm','"thunderstorm"[All Fields] OR "thunderstorms"[All Fields]'],
['Climate Change','"climate change"[MeSH Terms] OR ("climate"[All Fields] AND "change"[All Fields]) OR "climate change"[All Fields]'],
['Climatic Processes','"climatic processes"[MeSH Terms] OR ("climatic"[All Fields] AND "processes"[All Fields]) OR "climatic processes"[All Fields]'],
['Altitude','"altitude"[MeSH Terms] OR "altitude"[All Fields] OR "altitudes"[All Fields]'],
['Weather','"weather"[MeSH Terms] OR "weather"[All Fields] OR "weatherability"[All Fields] OR "weatherable"[All Fields] OR "weathered"[All Fields] OR "weathering"[All Fields] OR "weathers"[All Fields]'],
['Eutrophication','"eutrophic"[All Fields] OR "eutrophicated"[All Fields] OR "eutrophication"[MeSH Terms] OR "eutrophication"[All Fields] OR "eutrophications"[All Fields] OR "eutrophics"[All Fields] OR "eutrophized"[All Fields]'],
['Meterology','"meteorology"[MeSH Terms] OR "meteorology"[All Fields]']
]

#rerun after for all terms and vector borne disease

searchList2 = [
#['Vector Borne Diseases ','"vector borne diseases"[MeSH Terms] OR ("vector"[All Fields] AND "borne"[All Fields] AND "diseases"[All Fields]) OR "vector borne diseases"[All Fields]'],
#['Dengue','"dengue"[MeSH Terms] OR "dengue"[All Fields] OR "dengue\'s"[All Fields]'],
#['Malaria','"malaria"[MeSH Terms] OR "malaria"[All Fields] OR "malarias"[All Fields] OR "malaria\'s"[All Fields] OR "malariae"[All Fields]'],
#['Zika','"zika virus"[MeSH Terms] OR ("zika"[All Fields] AND "virus"[All Fields]) OR "zika virus"[All Fields] OR "zika"[All Fields] OR "zika virus infection"[MeSH Terms] OR ("zika"[All Fields] AND "virus"[All Fields] AND "infection"[All Fields]) OR "zika virus infection"[All Fields]'],
#['Chikugunya','"chikungunya fever"[MeSH Terms] OR ("chikungunya"[All Fields] AND "fever"[All Fields]) OR "chikungunya fever"[All Fields] OR "chikungunya"[All Fields]'],
#['Leprospirosis','"leptospirosis"[MeSH Terms] OR "leptospirosis"[All Fields] OR "leptospiroses"[All Fields]'],
#['Cholera','"cholera"[MeSH Terms] OR "cholera"[All Fields] OR "choleras"[All Fields] OR "cholera\'s"[All Fields] OR "cholerae"[All Fields] OR "cholerae\'s"[All Fields] OR "choleraic"[All Fields]'],
['Rift Valley/ Rift Valley Fever','"rift valley fever"[MeSH Terms] OR ("rift"[All Fields] AND "valley"[All Fields] AND "fever"[All Fields]) OR "rift valley fever"[All Fields]'],
#['Plague','"plague"[MeSH Terms] OR "plague"[All Fields] OR "plagues"[All Fields]'],
#['Diarrhea','"diarrhea"[MeSH Terms] OR "diarrhea"[All Fields] OR "diarrheas"[All Fields] OR "diarrhoea"[All Fields] OR "diarrhoeas"[All Fields]'],
#['Hantavirus Pulmonary Syndrome','"hantavirus pulmonary syndrome"[MeSH Terms] OR ("hantavirus"[All Fields] AND "pulmonary"[All Fields] AND "syndrome"[All Fields]) OR "hantavirus pulmonary syndrome"[All Fields]'],
#['Hemorrhagic Fever with Renal Syndrome','"haemorrhagic fever with renal syndrome"[All Fields] OR "hemorrhagic fever with renal syndrome"[MeSH Terms] OR ("hemorrhagic"[All Fields] AND "fever"[All Fields] AND "renal"[All Fields] AND "syndrome"[All Fields]) OR "hemorrhagic fever with renal syndrome"[All Fields]'],
#['Respiratory Syncitial Virus (RSV)','"respiratory syncytial viruses"[MeSH Terms] OR ("respiratory"[All Fields] AND "syncytial"[All Fields] AND "viruses"[All Fields]) OR "respiratory syncytial viruses"[All Fields] OR ("respiratory"[All Fields] AND "syncytial"[All Fields] AND "virus"[All Fields] AND "rsv"[All Fields]) OR "respiratory syncytial virus rsv"[All Fields]'],
#['Influenza','"influenza\'s"[All Fields] OR "influenza, human"[MeSH Terms] OR ("influenza"[All Fields] AND "human"[All Fields]) OR "human influenza"[All Fields] OR "influenza"[All Fields] OR "influenzae"[All Fields] OR "influenzas"[All Fields]'],
#['Vibrio ','"vibrio"[MeSH Terms] OR "vibrio"[All Fields] OR "vibrios"[All Fields]'],
#['Ebola','"ebola\'s"[All Fields] OR "hemorrhagic fever, ebola"[MeSH Terms] OR ("hemorrhagic"[All Fields] AND "fever"[All Fields] AND "ebola"[All Fields]) OR "ebola hemorrhagic fever"[All Fields] OR "ebola"[All Fields] OR "ebolavirus"[MeSH Terms] OR "ebolavirus"[All Fields]'],
#['Schistosomiasis','"schistosomiasis"[MeSH Terms] OR "schistosomiasis"[All Fields] OR "schistosomiases"[All Fields]'],
#['Tick borne disease','"tick-borne diseases"[MeSH Terms] OR ("tick-borne"[All Fields] AND "diseases"[All Fields]) OR "tick-borne diseases"[All Fields] OR ("tick"[All Fields] AND "borne"[All Fields] AND "disease"[All Fields]) OR "tick borne disease"[All Fields]'],
#['Chagas','"chaga"[All Fields] OR "chaga\'s"[All Fields] OR "chagas"[All Fields] OR "chagas\'s"[All Fields]'],
#['Filariasis','"filariasis"[MeSH Terms] OR "filariasis"[All Fields] OR "filariases"[All Fields]'],
#['Trypanosomiasis (tsetse flies - Glossina sp)','"trypanosomiasis"[MeSH Terms] OR "trypanosomiasis"[All Fields] OR "trypanosomiases"[All Fields]'],
#['Yellow fever','"yellow fever"[MeSH Terms] OR ("yellow"[All Fields] AND "fever"[All Fields]) OR "yellow fever"[All Fields]'],
#['Aedes','"aedes"[MeSH Terms] OR "aedes"[All Fields]'],
#['Anopheles','"anophele"[All Fields] OR "anopheles"[MeSH Terms] OR "anopheles"[All Fields]'],
#['Culex','"culex"[MeSH Terms] OR "culex"[All Fields]'],
#['Leishmaniasis','"leishmaniasis"[MeSH Terms] OR "leishmaniasis"[All Fields] OR "leishmaniases"[All Fields] OR "leishmaniasis vaccines"[MeSH Terms] OR ("leishmaniasis"[All Fields] AND "vaccines"[All Fields]) OR "leishmaniasis vaccines"[All Fields]'],
#['Salmonellosis','"salmonella infections"[MeSH Terms] OR ("salmonella"[All Fields] AND "infections"[All Fields]) OR "salmonella infections"[All Fields] OR "salmonellosis"[All Fields] OR "salmonella food poisoning"[MeSH Terms] OR ("salmonella"[All Fields] AND "food"[All Fields] AND "poisoning"[All Fields]) OR "salmonella food poisoning"[All Fields]'],
#['Giardiasis','"giardiasis"[MeSH Terms] OR "giardiasis"[All Fields] OR "giardiases"[All Fields]'],
#['new and emerging infectious diseases','"communicable diseases, emerging"[MeSH Terms] OR ("communicable"[All Fields] AND "diseases"[All Fields] AND "emerging"[All Fields]) OR "emerging communicable diseases"[All Fields] OR ("emerging"[All Fields] AND "infectious"[All Fields] AND "diseases"[All Fields]) OR "emerging infectious diseases"[All Fields]'],
#['climate-sensitive infectious diseases','"communicable diseases"[MeSH Terms] OR ("communicable"[All Fields] AND "diseases"[All Fields]) OR "communicable diseases"[All Fields] OR ("infectious"[All Fields] AND "diseases"[All Fields]) OR "infectious diseases"[All Fields]'],
#['allergic disease','"allergic"[All Fields] OR "allergical"[All Fields] OR "allergically"[All Fields] OR "allergics"[All Fields] OR "allergization"[All Fields] OR "allergizing"[All Fields]'],
#['Onchocercosis','"onchocerciasis"[MeSH Terms] OR "onchocerciasis"[All Fields] OR "onchocercosis"[All Fields]'],
#['babesiosis','"babesiosis"[MeSH Terms] OR "babesiosis"[All Fields] OR "babesioses"[All Fields]'],
#['rabies','"rabies"[MeSH Terms] OR "rabies"[All Fields'],
#['anaplasmosis','"anaplasmosis"[MeSH Terms] OR "anaplasmosis"[All Fields] OR "anaplasmoses"[All Fields]'],
#['Campylobacter infection','"campylobacter infections"[MeSH Terms] OR ("campylobacter"[All Fields] AND "infections"[All Fields]) OR "campylobacter infections"[All Fields] OR ("campylobacter"[All Fields] AND "infection"[All Fields]) OR "campylobacter infection"[All Fields]'],
#['Borreliosis','"borrelia infections"[MeSH Terms] OR ("borrelia"[All Fields] AND "infections"[All Fields]) OR "borrelia infections"[All Fields] OR "borreliosis"[All Fields]'],
#['West Nile Fever','"west nile fever"[MeSH Terms] OR ("west"[All Fields] AND "nile"[All Fields] AND "fever"[All Fields]) OR "west nile fever"[All Fields]'],
#['Botulism','"botulism"[MeSH Terms] OR "botulism"[All Fields]'],
#['Anthrax','"anthrax"[MeSH Terms] OR "anthrax"[All Fields]'],
#['Clostridiosis','"clostridium infections"[MeSH Terms] OR ("clostridium"[All Fields] AND "infections"[All Fields]) OR "clostridium infections"[All Fields] OR "clostridiosis"[All Fields]'],
#['Pasteurellosis','"pasteurella infections"[MeSH Terms] OR ("pasteurella"[All Fields] AND "infections"[All Fields]) OR "pasteurella infections"[All Fields] OR "pasteurellosis"[All Fields]'],
#['Parapoxvirus','"parapoxvirus"[MeSH Terms] OR "parapoxvirus"[All Fields] OR "parapoxviruses"[All Fields]'],
#['Pestivirus','"pestivirus"[MeSH Terms] OR "pestivirus"[All Fields] OR "pestiviruses"[All Fields]'],
#['Necrobacillosis','"fusobacterium infections"[MeSH Terms] OR ("fusobacterium"[All Fields] AND "infections"[All Fields]) OR "fusobacterium infections"[All Fields] OR "necrobacillosis"[All Fields]'],
#['Alphaherpes virus','"alphaherpesvirus"[All Fields]'],
#['Gammaherpes virus','"gammaherpesvirus"[All Fields]'],
#['Clostridiosis','"clostridium infections"[MeSH Terms] OR ("clostridium"[All Fields] AND "infections"[All Fields]) OR "clostridium infections"[All Fields] OR "clostridiosis"[All Fields]'],
#['Cryptosporidiosis','"cryptosporidiosis"[MeSH Terms] OR "cryptosporidiosis"[All Fields] OR "cryptosporidioses"[All Fields]'],
#['drug-resistant infections','"drug resistance"[MeSH Terms] OR ("drug"[All Fields] AND "resistance"[All Fields]) OR "drug resistance"[All Fields] OR ("drug"[All Fields] AND "resistant"[All Fields]) OR "drug resistant"[All Fields]'],
#['epidemic','"epidemic\'s"[All Fields] OR "epidemical"[All Fields] OR "epidemically"[All Fields] OR "epidemicity"[All Fields] OR "epidemics"[MeSH Terms] OR "epidemics"[All Fields] OR "epidemic"[All Fields] OR "epidemiology"[Subheading] OR "epidemiology"[All Fields]'],
#['pandemic','"pandemic\'s"[All Fields] OR "pandemically"[All Fields] OR "pandemicity"[All Fields] OR "pandemics"[MeSH Terms] OR "pandemics"[All Fields] OR "pandemic"[All Fields]'],
#['disease-escalation','"disease-escalation"[All Fields]'],
#['Tuberculosis','"tuberculosi"[All Fields] OR "tuberculosis"[MeSH Terms] OR "tuberculosis"[All Fields] OR "tuberculoses"[All Fields] OR "tuberculosis\'s"[All Fields]'],
#['neglected tropical diseases','("neglect"[All Fields] OR "neglected"[All Fields] OR "neglectful"[All Fields] OR "neglecting"[All Fields] OR "neglects"[All Fields]) AND ("tropic"[All Fields] OR "tropical"[All Fields] OR "tropicalization"[All Fields] OR "tropically"[All Fields] OR "tropics"[All Fields]) AND ("disease"[MeSH Terms] OR "disease"[All Fields] OR "diseases"[All Fields] OR "disease s"[All Fields] OR "diseased"[All Fields])'],
]

searchList3 = [
 ['prediction','"predict"[All Fields] OR "predictabilities"[All Fields] OR "predictability"[All Fields] OR "predictable"[All Fields] OR "predictably"[All Fields] OR "predicted"[All Fields] OR "predicting"[All Fields] OR "prediction"[All Fields] OR "predictions"[All Fields] OR "predictive"[All Fields] OR "predictively"[All Fields] OR "predictiveness"[All Fields] OR "predictives"[All Fields] OR "predictivities"[All Fields] OR "predictivity"[All Fields] OR "predicts"[All Fields]'],
 ['forecast','"forecasted"[All Fields] OR "forecaster"[All Fields] OR "forecasters"[All Fields] OR "forecasting"[MeSH Terms] OR "forecasting"[All Fields] OR "forecast"[All Fields] OR "forecasts"[All Fields] OR "trends"[Subheading] OR "trends"[All Fields]'],
 ['simulation','"computer simulation"[MeSH Terms] OR ("computer"[All Fields] AND "simulation"[All Fields]) OR "computer simulation"[All Fields] OR "simulation"[All Fields] OR "simul"[All Fields] OR "simulate"[All Fields] OR "simulated"[All Fields] OR "simulates"[All Fields] OR "simulating"[All Fields] OR "simulation\'s"[All Fields] OR "simulational"[All Fields] OR "simulations"[All Fields] OR "simulative"[All Fields] OR "simulator"[All Fields] OR "simulator\'s"[All Fields] OR "simulators"[All Fields]'],
 ['ensemble','"ensemble"[All Fields] OR "ensemble\'s"[All Fields] OR "ensembled"[All Fields] OR "ensembles"[All Fields] OR "ensembling"[All Fields]'],
 ['artificial intelligence','"artificial intelligence"[MeSH Terms] OR ("artificial"[All Fields] AND "intelligence"[All Fields]) OR "artificial intelligence"[All Fields]'],
 ['INLA','INLA'],
 ['mechanistic','"mechanistic"[All Fields] OR "mechanistically"[All Fields] OR "mechanistics"[All Fields]'],
 ['suitability','"suitabilities"[All Fields] OR "suitability"[All Fields] OR "suitable"[All Fields] OR "suitably"[All Fields]'],
 ['species distribution model','"geospatial"[All Fields] OR "geospatially"[All Fields]'],
 ['geospatial','"geospatial"[All Fields] OR "geospatially"[All Fields]'],
 ['spatial','"spatial"[All Fields] OR "spatialization"[All Fields] OR "spatializations"[All Fields] OR "spatialized"[All Fields] OR "spatially"[All Fields]'],
 ['machine learning','"machine learning"[MeSH Terms] OR ("machine"[All Fields] AND "learning"[All Fields]) OR "machine learning"[All Fields]'],
 ['artificial intelligence','"artificial intelligence"[MeSH Terms] OR ("artificial"[All Fields] AND "intelligence"[All Fields]) OR "artificial intelligence"[All Fields]'],
 ['neural network','"neural networks, computer"[MeSH Terms] OR ("neural"[All Fields] AND "networks"[All Fields] AND "computer"[All Fields]) OR "computer neural networks"[All Fields] OR ("neural"[All Fields] AND "network"[All Fields]) OR "neural network"[All Fields]'],
 ['natural language processing','"natural language processing"[MeSH Terms] OR ("natural"[All Fields] AND "language"[All Fields] AND "processing"[All Fields]) OR "natural language processing"[All Fields]'],
 ['deep learning','"deep learning"[MeSH Terms] OR ("deep"[All Fields] AND "learning"[All Fields]) OR "deep learning"[All Fields]'],
 ['supervised machine learning','"supervised machine learning"[MeSH Terms] OR ("supervised"[All Fields] AND "machine"[All Fields] AND "learning"[All Fields]) OR "supervised machine learning"[All Fields]'],
 ['support vector machine','"support vector machine"[MeSH Terms] OR ("support"[All Fields] AND "vector"[All Fields] AND "machine"[All Fields]) OR "support vector machine"[All Fields]'],
 ['unsupervised machine learning','"unsupervised machine learning"[MeSH Terms] OR ("unsupervised"[All Fields] AND "machine"[All Fields] AND "learning"[All Fields]) OR "unsupervised machine learning"[All Fields]'],
 ['Data Mining','"data mining"[MeSH Terms] OR ("data"[All Fields] AND "mining"[All Fields]) OR "data mining"[All Fields]'],
 ['predictive analytics','("predict"[All Fields] OR "predictabilities"[All Fields] OR "predictability"[All Fields] OR "predictable"[All Fields] OR "predictably"[All Fields] OR "predicted"[All Fields] OR "predicting"[All Fields] OR "prediction"[All Fields] OR "predictions"[All Fields] OR "predictive"[All Fields] OR "predictively"[All Fields] OR "predictiveness"[All Fields] OR "predictives"[All Fields] OR "predictivities"[All Fields] OR "predictivity"[All Fields] OR "predicts"[All Fields]) AND ("analyte"[All Fields] OR "analyte s"[All Fields] OR "analytes"[All Fields] OR "analytic"[All Fields] OR "analytical"[All Fields] OR "analytically"[All Fields] OR "analyticity"[All Fields] OR "analytics"[All Fields])'],
 ['stochastic modeling','("stochastic"[All Fields] OR "stochastical"[All Fields] OR "stochastically"[All Fields] OR "stochasticities"[All Fields] OR "stochasticity"[All Fields] OR "stochastics"[All Fields]) AND ("model"[All Fields] OR "model s"[All Fields] OR "modeled"[All Fields] OR "modeler"[All Fields] OR "modeler s"[All Fields] OR "modelers"[All Fields] OR "modeling"[All Fields] OR "modelings"[All Fields] OR "modelization"[All Fields] OR "modelizations"[All Fields] OR "modelize"[All Fields] OR "modelized"[All Fields] OR "modelled"[All Fields] OR "modeller"[All Fields] OR "modellers"[All Fields] OR "modelling"[All Fields] OR "modellings"[All Fields] OR "models"[All Fields])'],
 ['SIR ','"sir"[All Fields]'],
 ['compartmental model','("compartmental"[All Fields] OR "compartmentalization"[All Fields] OR "compartmentalizations"[All Fields] OR "compartmentalize"[All Fields] OR "compartmentalized"[All Fields] OR "compartmentalizes"[All Fields] OR "compartmentalizing"[All Fields] OR "compartmentally"[All Fields] OR "compartmentation"[All Fields] OR "compartmentations"[All Fields]) AND ("model"[All Fields] OR "model s"[All Fields] OR "modeled"[All Fields] OR "modeler"[All Fields] OR "modeler s"[All Fields] OR "modelers"[All Fields] OR "modeling"[All Fields] OR "modelings"[All Fields] OR "modelization"[All Fields] OR "modelizations"[All Fields] OR "modelize"[All Fields] OR "modelized"[All Fields] OR "modelled"[All Fields] OR "modeller"[All Fields] OR "modellers"[All Fields] OR "modelling"[All Fields] OR "modellings"[All Fields] OR "models"[All Fields])'],
 ['differential equations','("cell differentiation"[MeSH Terms] OR ("cell"[All Fields] AND "differentiation"[All Fields]) OR "cell differentiation"[All Fields] OR "differentiated"[All Fields] OR "differentiation"[All Fields] OR "differential"[All Fields] OR "differentials"[All Fields] OR "differentiate"[All Fields] OR "differentiates"[All Fields] OR "differentiating"[All Fields] OR "differentiational"[All Fields] OR "differentiations"[All Fields] OR "differentiative"[All Fields]) AND ("equation"[All Fields] OR "equation s"[All Fields] OR "equations"[All Fields])'],
 ['Bayesian  ','Bayesian: "bayesian"[All Fields] OR "bayesianism"[All Fields] OR "bayesians"[All Fields]'],
 ['logistic ','"logistical"[All Fields] OR "logistically"[All Fields] OR "organization and administration"[MeSH Terms] OR ("organization"[All Fields] AND "administration"[All Fields]) OR "organization and administration"[All Fields] OR "logistic"[All Fields] OR "logistics"[All Fields]'],
 ['Representative Concentration Pathway (RCP)','"Representative Concentration Pathway"[All Fields]'],
 ['General Circulation Model','"General Circulation Model"[All Fields]'],
 ['Bayesian Regression Tree','"Bayesian Regression Tree"[All Fields]'],
]

#searchList3 = [
#	['R package','R package'],
#	['Python','Python'],
#	['open source','open source'],
#	['software','software'],
#	['database','database'],
#	['google earth engine','google earth engine'],
#	['javascript','javascript'],
#	['github','github'],
#	['gitlab','gitlab'],
#	['Open Science Framework','Open Science Framework'],
#]


#searchList1 = [['climate','climate']]
#searchList2 = [['vector borne diseases','"vector borne diseases"[MeSH Terms] OR ("vector"[All Fields] AND "borne"[All Fields] AND "diseases"[All Fields]) OR "vector borne diseases"[All Fields] OR ("vector"[All Fields] AND "borne"[All Fields] AND "disease"[All Fields]) OR "vector borne disease"[All Fields]']]
#database to search against either "pubmed" or "pmc"
db = "pubmed"

#whether you want to test the search and not write to the database
test = False;

###########
#processing
###########

#load database configuration

with open('local_config.json') as json_file:
	config = json.load(json_file)

#connect to do database and check if paper is already added.  If not add to todo list
conn = psycopg2.connect(host=config['endpoint'],database=config['database'], user=config['username'], password=config['password'])

cur = conn.cursor()

for search1 in searchList1:
	for search2 in searchList2:
		for search3 in searchList3:

			searchTerm = '('+search1[1] + ') AND (' + search2[1] + ') AND (' + search3[1] + ')'
			searchID = search1[0] + ' + ' + search2[0] + ' + ' + search3[0]
			
			#encode parameters
			params = {"db":db,"term":searchTerm,"tool":"tool_landscape_mapping","email":"simon@hetco.io","dateType":"pdat","mindate":"2011/01/01","maxdate":"2022/01/01","retmax":50000}
			#params = {"term":searchTerm,"tool":"tool_landscape_mapping","email":"simon@hetco.io","retmax":50000}
			paramsEncode = urllib.parse.urlencode(params)

			#create URL
			url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{paramsEncode}"

			#request content
			contents = urllib.request.urlopen(url).read()

			#extract PMIDs from results
			soup = BeautifulSoup(contents,'html.parser')
			numresults = len(soup.idlist.find_all('id'))
			results = []
			for pmid in soup.idlist.find_all('id'):
				results.append(pmid.get_text())
			print(searchTerm)
			print(results)

