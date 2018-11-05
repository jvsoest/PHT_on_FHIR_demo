import os
import json

endpointType = "FHIR"
if os.environ.get("endpointType") != None:
    endpointType = os.environ.get("endpointType")

endpointUrl = "http://hapi.fhir.org/baseDstu3"#"https://syntheticmass.mitre.org/fhir"
if os.environ.get("endpointUrl") != None:
    endpointUrl = os.environ.get("endpointUrl")

endpointToken = "my_web_app"#"my_app"
if os.environ.get("endpointToken") != None:
    endpointToken = os.environ.get("endpointToken")

outputJson = { }

if endpointType == "FHIR":
    import fhir
    outputJson = fhir.runCohortCounter(endpointUrl, endpointToken)
if endpointType == "SPARQL":
    import sparql
    outputJson = sparql.runCohortCounter(endpointUrl)

# Write output to file
with open('output.txt', 'w') as f:
    f.write(json.dumps(outputJson))