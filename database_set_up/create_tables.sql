CREATE TABLE paper (
  paper_id serial PRIMARY KEY
, pmid integer
, pmcid integer
, semanticid text
, papertitle text
, abstract text
, reviewed text
, influence integer
, numAuthors integer
, search_id text
);

CREATE TABLE todo (
  todo_id serial PRIMARY KEY
, pmid integer
, pmcid integer
, semanticid text
, search_id text
);

CREATE TABLE department (
  department_id serial PRIMARY KEY
, department_name text
);

CREATE TABLE paper_department (
  paper_id integer REFERENCES paper(paper_id)
, department_id integer REFERENCES department(department_id)
);

CREATE TABLE institute (
  institute_id serial PRIMARY KEY
, institute_name text
, score integer
, country integer
, lat numeric
, lon numeric
);

CREATE TABLE department_institute (
  department_id integer REFERENCES department(department_id)
, institute_id integer REFERENCES institute(institute_id)
);

CREATE TABLE keyword (
  keyword_id serial PRIMARY KEY
, keytext text
, meshorkey text
);

CREATE TABLE keyword_paper (
  keyword_id integer
, paper_id integer
);

CREATE TABLE todo_parked (
  todo_id integer PRIMARY KEY
, pmid integer
, pmcid integer
, semanticid text
, search_id text
);

CREATE TABLE country (
  country_id serial PRIMARY KEY
, country text
, subregion text
, continent text
, northsouth text

)