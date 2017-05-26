from SPARQLWrapper import SPARQLWrapper, JSON, POST
from docs import conf, sparql_templates as sparqlt, rdf_templates as rdft
import os


def load_turtle(file_path, turtle_str):
    with open(file_path, 'w') as rdf_file:
        rdf_file.write(turtle_str)
    query = 'LOAD <file://' + file_path + '>'
    sparql = SPARQLWrapper(conf.SPARQL_UPLOAD_ENDPOINT)
    sparql.setQuery(query)
    sparql.setMethod(POST)
    sparql.query()
    os.remove(file_path)


def get_turtle_uri(uri, recursive):
    sparql = SPARQLWrapper(conf.SPARQL_QUERY_ENDPOINT)
    query = sparqlt.GET_ALL_URI.format(uri=uri)
    sparql.setQuery(query)
    sparql.query()
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    turtle = ''

    for result in results['results']['bindings']:
        property = result['property']['value']
        if 'hasValue' in result:
            related_turtle = ''
            if result['hasValue']['type'] == 'literal':
                value = '"' + result['hasValue']['value'] + '"'
                value = value.encode('utf8')
            else:
                value = '<' + result['hasValue']['value'] + '>'
                if recursive:
                    related_turtle += '\n\n' + get_turtle_uri(result['hasValue']['value'], False) + '\n\n'
            turtle += rdft.TURTLE_TEMPLATES['hasValue'].format(uri=uri,
                                                               property=property,
                                                               value=value)
            turtle += related_turtle
        else:
            turtle += rdft.TURTLE_TEMPLATES['isValueOf'].format(uri=uri,
                                                                property=property,
                                                                subject=result['isValueOf']['value'])
            if recursive:
                turtle += '\n\n' + get_turtle_uri(result['isValueOf']['value'], False) + '\n\n'
    return turtle




