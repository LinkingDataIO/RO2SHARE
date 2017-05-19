USER_EXIST_QUERY = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
ASK {{ <http://orcid.org/{orcid}>  foaf:name|rdfs:label ?name .
  FILTER(regex(lcase(?name), lcase("{name}") )) }}
"""

USER_ROS = """
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?uri ?title {{
  ?uri dcterms:creator <{orcid}> .
  ?uri dcterms:title ?title .
}}
"""