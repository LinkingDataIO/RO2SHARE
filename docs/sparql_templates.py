USER_EXIST_QUERY = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
ASK {{ <http://orcid.org/{orcid}>  foaf:name ?name .
  FILTER(regex(?name, "{name}" )) }}
"""