from fhirclient import client
from fhirclient.models.patient import Patient
import fhirclient.models.condition as c
from fhirclient.models import fhirsearch
from datetime import datetime
from datetime import date

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
count = 0
age_i = 0
age = 0
num = 0

search = Patient.where(struct={'gender': 'unknown'})

bundle1 = search.perform_resources(smart.server)
bundle2 = search.perform_resources(smart2.server)


for patients in bundle1:
    count = count + 1

print(count)

for patients in bundle2:
    count = count + 1

def calculate_age(born):
    # convert str to datetime format
    dob = datetime.strptime(born, "%Y-%m-%d")
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


for patients in bundle1:
    entry = patients.as_json()
    dob = entry['birthDate']
    age_i = calculate_age(dob)
    age = age+age_i

for patients in bundle2:
    entry = patients.as_json()
    dob = entry['birthDate']
    age_i = calculate_age(dob)
    age = age+age_i

avg_age = age/count
print(age)
print('Total number of patients matching the criteria is', count, 'avg age is', avg_age)
