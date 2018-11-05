from fhirclient import client
from fhirclient.models.patient import Patient
import fhirclient.models.condition as c
from fhirclient.models import fhirsearch
from datetime import datetime
from datetime import date

def runCohortCounter(endpointUrl, endpointToken):
    #connect to FHIR server
    smart = client.FHIRClient(settings={
        'app_id': endpointToken,
        'api_base': endpointUrl
    })

    search = Patient.where(struct={'gender': 'unknown'})
    cohort = search.perform_resources(smart.server)

    cohortSize = len(cohort)

    ageSum = 0

    def calculate_age(born):
        # convert str to datetime format
        dob = datetime.strptime(born, "%Y-%m-%d")
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    # Loop over all patients in bundle
    for patients in cohort:
        entry = patients.as_json()
        dob = entry['birthDate']
        age_i = calculate_age(dob)
        ageSum = ageSum+age_i

    print("Cohort size: %s" % cohortSize)

    # Calculate mean age
    meanAge = None
    if cohortSize > 0:
        meanAge = ageSum / cohortSize
        print("Mean age in cohort: %s" % meanAge)

    return {
        'cohortCount': cohortSize,
        'meanAge': meanAge
    }