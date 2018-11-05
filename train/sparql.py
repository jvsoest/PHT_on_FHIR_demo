from SPARQLWrapper import SPARQLWrapper, JSON
import json


def runCohortCounter(endpointUrl):
    sparql = SPARQLWrapper(endpointUrl)
    sparql.setQuery("""
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
        prefix roo: <http://www.cancerdata.org/roo/>
        prefix icd: <http://purl.bioontology.org/ontology/ICD10/>

        select ?patient ?ageDiagnosis
        where {
            ?patient rdf:type ncit:C16960.
            ?patient roo:100008 ?disease.
            ?disease rdf:type icd:C20.
            
            ?patient roo:100016 ?ageDiagnosisRes.
            ?ageDiagnosisRes roo:100042 ?ageDiagnosis.
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    sumAge = 0
    # sum all ages
    for result in results["results"]["bindings"]:
        sumAge = sumAge + int(result["ageDiagnosis"]["value"])

    # divide sumAge by all patients
    cohortSize = len(results["results"]["bindings"])
    meanAge = sumAge / cohortSize

    # write output to file
    return {
        'cohortCount': cohortSize,
        'meanAge': meanAge
    }