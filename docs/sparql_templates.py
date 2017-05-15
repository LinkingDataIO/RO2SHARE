USER_EXIST_QUERY = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
ASK {{ <http://orcid.org/{orcid}>  foaf:name ?name .
  FILTER(regex(?name, "{name}" )) }}
"""

USER_ROS = """
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?uri ?title {{
  ?uri dcterms:creator <{orcid}> .
  ?uri dcterms:title ?title .
}}
"""