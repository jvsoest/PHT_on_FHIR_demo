from fhirclient import client
from fhirclient.models.patient import Patient
from fhirclient.models import fhirsearch as S
from datetime import datetime
from datetime import date
from fhirclient.models import fhirsearch


def perform_in(srch_str, server,apiBase):
    """ Execute the search URL against the given server.

    :param server: The server against which to perform the search
    :returns: A Bundle resource
    """

    from fhirclient.models import bundle
    if server is None:
        raise Exception("Need a server to perform search")
    resources = []
    bundleBase = server.request_json(srch_str)
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

def runCohortCounter(endpointUrl, endpointToken):
    #connect to FHIR server
    smart = client.FHIRClient(settings={
        'app_id': endpointToken,
        'api_base': endpointUrl
    })

    urlBase = endpointUrl
    #Patients diagnosed with diabetes
    print('Patient cohort for Diabetes')
    search_str = 'Condition?_include=Condition:patient&code=73211009,399144008,11530004,9414007,315051004,9414007,15771004'

   # print('Patient cohort for asthma')
    #search_str = 'Condition?_include=Condition:patient&code=195917001'
    cohort = perform_in(search_str,smart.server,urlBase)

    results = len(cohort)
    cohortSize = int(results/2)
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
            results = results - 1
    
    print("Cohort size after eliminating patients with no age data: %s" % results)


    # Calculate mean age
    meanAge = None
    if cohortSize > 0:
        meanAge = ageSum / results
        print("Mean age in cohort: %s" % meanAge)

    return {
        'cohortCount': results,
        'meanAge': meanAge
    }