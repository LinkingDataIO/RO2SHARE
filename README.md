# RO2SHARE
Digital assets are more valuable when they are part of a network rather than when they live in isolation; this is true also for research related assets. RO2SHARE delivers a curatorial infrastructure for Research Digital Assets, A.K.A Research objects. We aim to i) facilitate the definition of "ownership" over these assets and ii) make it possible for researchers to establish relations across these assets. We are using semantic web technology, e.g. RDF, in order to expose the resulting datasets; we are using ontologies, e.g. DC, RO, in order to represent the RDAs and the relations amongst them. Ours is an incremental approach, initially the triplets are related to the RDAs, "ownership" is then added to the graph; depending on the type of RDA, e.g. paper, software, figure, dataset, we are adding related triplets from external sources, e.g. Biotea (RDF for PMC), Colil (citations in context) and DBPEDIA. The resulting data from the brief interaction between the end user and the digital assets being managed over our interface is open and it is exposed over our SPARQL endpoint. This project delivers data infrastructure, the GUI is just for demostration purposes; the UX will be part of our future work. We are using SHARE data because it aggregates several sources; we are using the ORCID API as our authoritative ID provider and validator. Our work reuses datamodels and concepts from the Open Archives Initiative Object Reuse and Exchange and the rmap-project. 

## Web service Installation
Before installing make sure that you have included a conf.py file in the docs/ path. There is an example under docs/conf_template.py. You can copy and edit that file in order to install your local RO2SHARE.
### Requirements
You will need to have a SPARQL Endpoint (e.g. Fuseki Triple Store) up and running in order to run this web service.

- Download Apache Fuseki from the [Apache Downloads Web site](https://jena.apache.org/download/#jena-fuseki)
- Uncompress it
```bash
cd apache-jena-fuseki-3.4.0/
./fuseki-server
```
The go to http://localhost:3030 and create a new dataset called 'ro2share'.
### Using Virtual Enviroment
```bash
sudo apt-get update -y
sudo apt-get install -y python-pip python-dev build-essential libxml2-dev libxslt1-dev zlib1g-dev
git clone https://github.com/LinkingDataIO/RO2SHARE.git
cd RO2SHARE
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
python run.py
```

### Using the Dockerfile
Replace the 'localhost' reference in the SPARQL\_QUERY\_ENDPOINT and SPARQL\_UPLOAD\_ENDPOINT values  in your docs/conf.py with the IP Address of your Docker Host corresponding to the Network Interface docker0.

```bash
git clone https://github.com/LinkingDataIO/RO2SHARE.git
cd RO2SHARE
sudo docker build -t username:RO2SHARE .
sudo docker run -p 8080:8080 username:RO2SHARE
```
## Client Installation
The client is available at [LinkingDataIO/RO2SHARE-client](https://github.com/LinkingDataIO/RO2SHARE-client). Clone it and Include your ORCID APP Client ID in src/environments/enviroment.ts and src/environments/enviroment.prod.ts

### Using NPM
```bash
git clone https://github.com/LinkingDataIO/RO2SHARE-client.git
cd RO2SHARE-client
npm install
npm start
```

### Using Dockerfile
```bash
git clone https://github.com/LinkingDataIO/RO2SHARE-client.git
cd RO2SHARE-client
sudo docker build -t username:RO2SHARE-client .
sudo docker run -p 4200:4200 -v /tmp:/tmp username:RO2SHARE-client
```

## Use cases
### Expanding the graph on PMC papers
Our is an incremental approach that makes use of linked data in order to expand the graph of triplets that are related to a 
Research Digital Asset. Depenidng on the type of RDA, we use different sources. This example ilustrates the use of the Biotea dataset;
this is a 

### VIVO
The VIVO dataset represents scholars within academic enviroments. It has been built over an ontology that represents profesors, researchers, outcomes, organization,
publications, etc. Several universities are part of the VIVO effort, this makes VIVO an authoritative data source because universities are mantaining 
the information. Although VIVO is not heavy on ORCIDs, some VIVO records do have an ORCID. For our project, ORCID, identifiers in general,
is an anchor that helps us to expand related triplets in our graph.
User Story: as a researcher I want to bring my publications from my VIVO profile
Data Workflow
User Story: as a researcher I want to bring some specific items from my VIVO profile, e.g. vivo:overview
Data Workflow

### Institutions
These include, universities, research institutes, etc. 
User story: the research manager at University X wants to retrive a list of publications with their associated datasets for a 
given ORCID OR for a given name, e.g. Mike Conlon. 
User story: the research manager at University X wants to retrieve all datasets known for a 
given ORCID OR for a given name, e.g. Mike Conlon. 
User story: the research manager at University X wants to retrieve the triad "paper-dataset-software" for a 
given ORCID OR for a given name, e.g. Oscar Corcho. 

### Publishers
User story: the editor of a journal wants to ask the author for the triad "paper-software-dataset" 
Note: this assumes the paper has a DOI, so it is after the paper has been reviewed and a DOI has been assigned. 
It is also assumed that SHARE knows the dataset and the software for the author-ORCID. 
User story: the editor of a journal wants to ask the author for any material related to the submited paper

### Researchers
User story: as a researcher I want to retrieve a list of all my triads "paper-software-dataset" 
User story: as a researcher I want to retrive incomplete triads, e.g. "papers with dataset and no software" 
