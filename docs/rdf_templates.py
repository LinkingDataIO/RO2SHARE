PREFIXES = """
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix fabio: <http://purl.org/spar/fabio/> .
@prefix bibo: <http://purl.org/ontology/bibo/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix scoro: <http://purl.org/spar/scoro/> .
@prefix pro: <http://purl.org/spar/pro/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
"""

FABIO_TYPES = dict(article='Article', conference_paper='ConferencePaper')
FOAF_TYPES = dict(person='Person', organization='Organization', institution='Organization')

CREATIVE_WORK_TYPE = """
<{work_uri}> a fabio:{type} .
"""

CREATIVE_WORK_CREATOR = """
<{work_uri}> dcterms:creator <{creator_uri}> .
"""

CREATIVE_WORK_TITLE = """
<{work_uri}> dcterms:title "{title}" .
"""

CREATIVE_WORK_PUBLISHER = """
<{work_uri}> dcterms:publisher <{publisher_uri}> .
"""

CREATIVE_WORK_DOI = """
<{work_uri}> bibo:doi "{doi}" .
"""

CREATIVE_WORK_SEE_ALSO = """
<{work_uri}> owl:seeAlso <{web_site}> .
"""

CREATIVE_WORK_DESCRIPTION = """
<{work_uri}> dcterms:description "{description}" .
"""

CREATIVE_WORK_IDENTIFIER = """
<{work_uri}> dcterms:identifier <{identifier}> .
"""

PUBLISHER = """
<{publisher_uri}> a foaf:{type} .
<{publisher_uri}> foaf:name "{name}" .
"""

PERSON = """
<{contributor_uri}> a foaf:Person .
<{contributor_uri}> foaf:name "{name}" .
"""

AFFILIATION = """
<{affiliation_uri}> foaf:name "{name}" .
<{affiliation_uri}> a foaf:Organization .
"""

PERSON_WORK_AFFILIATION = """
<{person_uri}> pro:holdsRoleInTime <{person_uri_role}> .
<{person_uri_role}> a pro:RoleInTime ;
    pro:withRole scoro:affiliate ;
    pro:relatesToDocument
        <{work_uri}> ;
    pro:relatesToOrganization
        <{affiliation_uri}> .
"""

CREATIVE_WORK_TAG = """
<{work_uri}> dc:subject "{tag}" .
"""

