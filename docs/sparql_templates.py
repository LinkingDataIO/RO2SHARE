USER_EXIST_QUERY = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
ASK {{ <http://orcid.org/{orcid}>  foaf:name|rdfs:label ?name .
  FILTER(regex(lcase(?name), lcase("{name}") )) }}
"""

USER_ROS = """
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?uri ?title ?type {{
  ?uri dcterms:creator <{orcid}> .
  ?uri dcterms:title ?title .
  ?uri a ?type .
  FILTER(str(?type) != "http://rmap-project.org/rmap/terms/DiSCO")
}}
"""

USER_DISCOS = """
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX ore: <http://www.openarchives.org/ore/terms/>

SELECT ?uri ?title (GROUP_CONCAT(?name;separator=" | ") as ?titles) (GROUP_CONCAT(?object;separator="|") as ?objects)
{{
  ?uri dcterms:creator <{orcid}> .
  ?uri dc:description ?title .
  ?uri a <http://rmap-project.org/rmap/terms/DiSCO> .
  ?uri ore:aggregates ?object .
  ?object dcterms:title ?name .
}} GROUP BY ?uri ?title
"""

RO_EXIST = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
ASK {{
  ?s owl:sameAs <{share_url}> .
  ?s dcterms:creator <{orcid}> .
}}
"""

GET_ALL_URI = """
SELECT DISTINCT ?property ?hasValue ?isValueOf
WHERE {{
  {{ <{uri}> ?property ?hasValue }}
  UNION
  {{ ?isValueOf ?property <{uri}> }}
}}
"""

DELETE_DISCO = """
DELETE {{ <{disco_uri}> ?p ?o  }} WHERE {{ <{disco_uri}> ?p ?o }}
"""