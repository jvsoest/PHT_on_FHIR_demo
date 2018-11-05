from fhirclient import client
from fhirclient.models.patient import Patient
import fhirclient.models.condition as c
from fhirclient.models import fhirsearch
from datetime import datetime
from datetime import date

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

def runCohortCounter(endpointUrl, endpointToken):
    #connect to FHIR server
    smart = client.FHIRClient(settings={
        'app_id': endpointToken,
        'api_base': endpointUrl
    })

    #Patients diagnosed with diabetes
    print('Patient cohort for Diabetes')
    search_str = 'Patient?_has:Condition:subject:code:73211009,399144008,11530004,9414007,315051004,9414007,15771004,15777000,44054006'
    cohort = perform_in(search_str,smart.server)

    cohortSize = len(cohort)
    print("Retrieved cohort size %s" %cohortSize)

    ageSum = 0

    def calculate_age(born):
        # convert str to datetime format
        dob = datetime.strptime(born, "%Y-%m-%d")
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    # Loop over all patients in bundle
    for patients in cohort:
        entry = patients.as_json()
        if 'birthDate' in entry.keys():
            dob = entry['birthDate']
            age_i = calculate_age(dob)
            ageSum = ageSum+age_i
        else:
            cohortSize = cohortSize - 1
    
    print("Cohort size after eliminating patients with no age data: %s" % cohortSize)

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