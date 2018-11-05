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

server1 = {
    'app_id': 'my_web_app',
    'api_base': 'http://hapi.fhir.org/baseDstu3'
}

server2 = {
    'app_id': 'my_app',
    'api_base': 'https://syntheticmass.mitre.org/fhir'
}

smart = client.FHIRClient(settings=server1)
smart2 = client.FHIRClient(settings=server2)
count1 = 0
count2 = 0
age_i = 0
age = 0
num = 0

def perform_in(srch_str, server):
    """ Execute the search URL against the given server.

    :param server: The server against which to perform the search
    :returns: A Bundle resource
    """

    from fhirclient.models import bundle
    if server is None:
        raise Exception("Need a server to perform search")

    res = server.request_json(srch_str)
    bundle = bundle.Bundle(res)
    bundle.origin_server = server

    resources = []
    if bundle is not None and bundle.entry is not None:
        for entry in bundle.entry:
            resources.append(entry.resource)
    return resources

#Patients diagnosed with diabetes
search_str = 'Patient?_has:Condition:subject:code:73211009,399144008,11530004,9414007,315051004,9414007,15771004,15777000,44054006'

#Patients diagnosed with sinusitis
#search_str = 'Patient?_has:Condition:subject:code=444814009,75498004,36971009,40055000'

#Patients diagnosed with asthma
#search_str = 'Patient?_has:Condition:subject:code=195917001'

bundle1 = perform_in(search_str,smart.server)
bundle2 = perform_in(search_str,smart2.server)

cohortSize = len(bundle1) + len(bundle2)

if len(bundle1)!= 0:
    print("Cohorts retrieved from smart server is: %s" %len(bundle1))
else:
    print('No resources retrieved from Smart server')

if len(bundle2)!=0:
    print("Cohorts retrieved from smart server is: %s" % len(bundle2))
else:
    print('No resources retrieved from Synthetic mass server')

ageSum=0

def calculate_age(born):
    # convert str to datetime format
    dob = datetime.strptime(born, "%Y-%m-%d")
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

print("Cohort Size %s" %cohortSize)

# Loop over patients in bundle
for patients in bundle1:
    entry = patients.as_json()
    if 'birthDate' in entry.keys():
        dob = entry['birthDate']
        age_i = calculate_age(dob)
        ageSum = ageSum+age_i
    else:
        cohortSize =cohortSize-1

for patients in bundle2:
    entry = patients.as_json()
    if 'birthDate' in entry.keys():
        dob = entry['birthDate']
        age_i = calculate_age(dob)
        ageSum = ageSum+age_i
    else:
        cohortSize =cohortSize-1

print("Cohort size after eliminating patients with no age information: %s" % cohortSize)

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
