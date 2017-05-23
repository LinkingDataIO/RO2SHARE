from SPARQLWrapper import SPARQLWrapper, JSON, POST
from docs import conf


def load_turtle(file_path, turtle_str):
    with open(file_path, 'w') as rdf_file:
        rdf_file.write(turtle_str)
    query = 'LOAD <file://' + file_path + '>'
    sparql = SPARQLWrapper(conf.SPARQL_UPLOAD_ENDPOINT)
    sparql.setQuery(query)
    sparql.setMethod(POST)
    sparql.query()
