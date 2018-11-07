from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models import fhirsearch as S
from datetime import datetime
from datetime import date
from fhirclient.models import fhirsearch
import os
import json

from fhirclient.models import bundle
# Connection settings to server

server = {
    'app_id': 'my_web_app',
    'api_base': 'http://hapi.fhir.org/baseDstu3/'
}

baseUrl= server['api_base']
smart = client.FHIRClient(settings=server)


def perform_in(searchString, server, apiBase):
    """ Execute the search URL against the given server.

    :param server: The server against which to perform the search
    :returns: A Bundle resource
    """

    if server is None:
        raise Exception("Need a server to perform search")
    resources = []
    bundleBase = server.request_json(searchString)
    bundleCur = bundleBase

    from fhirclient.models import bundle
    bundle = bundle.Bundle(bundleBase)
    bundle.origin_server = server
    if bundle is not None and bundle.entry is not None:
        for entry in bundle.entry:
            resources.append(entry.resource)

    while True:
        if bundleCur['link'][1]['relation'] != 'previous':
            from fhirclient.models import bundle
            bundleAll = list()
            url = bundleCur['link'][1]['url']
            urlString = url.replace(apiBase, '')
            bundleNext = server.request_json(urlString)
            bundleN = bundle.Bundle(bundleNext)
            bundleN.origin_server = server
            if bundleN is not None and bundleN.entry is not None:
                  for entry in bundleN.entry:
                         resources.append(entry.resource)
            bundleCur = bundleNext
        else:
            break

    return resources

#Patients diagnosed with diabetes
#search_str = 'Patient?_has:Condition:subject:code:73211009,399144008,11530004,9414007,315051004,9414007,15771004,15777000,44054006'
search_str='Condition?_include=Condition:patient&code=195917001'

#Patients diagnosed with sinusitis
#search_str = 'Patient?_has:Condition:subject:code=444814009,75498004,36971009,40055000'

#Patients diagnosed with asthma
#search_str = 'Patient?_has:Condition:subject:code=195917001'

bundle = perform_in(search_str,smart.server,baseUrl)
cohortSize = len(bundle)/2

ageSum=0

def calculate_age(born):
    # convert str to datetime format
    dob = datetime.strptime(born, "%Y-%m-%d")
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

print("Cohort Size %s" %cohortSize)


# Loop over patients in bundle
for resources in bundle:
    json_res = resources.as_json()

    if 'birthDate' in json_res.keys():
        dob = json_res['birthDate']
        if 'deceasedBoolean' in json_res.keys():
            if 'deceasedDateTime' in json_res.keys():
                dod = json_res['deceasedDateTime']
        age_i = calculate_age(dob)
        ageSum = ageSum + age_i


# Calculate mean age
meanAge = None
if cohortSize > 0:
    meanAge = ageSum / cohortSize
    print("Mean age in cohort: %s" % meanAge)

# Write output to file
with open('output.txt', 'w') as f:
    f.write(json.dumps({
        'cohortCount': cohortSize,
        'meanAge': meanAge
    }))
