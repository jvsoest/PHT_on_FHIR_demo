# Personal Health Train on FHIR demo

Welcome to the Personal Health Train on FHIR demo. In this demo, we want to show how the Personal Health Train and FHIR can work together.

**tl/dr: see [control/pht_execution_notebook.ipynb](control/pht_execution_notebook.ipynb) to run the PHT cohort counter.**

The basic technical essence of the Personal Health Train is to use computational resources at the data source. This means:
* we can calculate information at the source
* we don't have to transfer data for calculation purposes, hence preserving patients' privacy
* we are able to support different data representation and query standards, as applications/calculations at the source can perform the conversion/transformation.

This repository is structured into two different folders:
* the application (in the [train](./train) folder)
* the control post for trains (in the [control](./control) folder)

## Train specifications
The train (application) is described in the [train](./train) folder. The main script in here is `run.py`, which reads environment variables indicating the endpoint type, URL and optional token. Based on the endpoint type, it selects the FHIR or SPARQL script and included query protocol. Finally, it will report the results in a text file (`output.txt`).

### FHIR query file
The FHIR endpoint is queried for all patients having Diabetes (all types), this code is available in `fhir.py`. Based on the FHIR endpoint result, the number of patients are counted, and the mean age in this cohort calculated.

### SPARQL query file
The sparql query file (`sparql.py`) contains a sparql query, which is being executed on the given endpoint URL. This query identifies patients with rectal cancer (ICD code C20) and requests the age at diagnosis. Afterwards, the number of patients (rows) are counted, and the mean age in this cohort calculated.

### Make a train using docker
The script to convert these analysis scripts into a docker container is available in `Dockerfile`. This creation can be executed by running `build.bat`, which builds an image based on the description in `Dockerfile` and sends this image to a central Docker repository. Afterwards, the data stations will pull the image from this repository, and execute the image (containing the analysis scripts and dependencies).

## Control post
The control post is defined in a Jupyter Notebook. This notebook can be executed by downloading the repository, navigating to the [control](./control) folder, and running the Jupyter Notebook command (`jupyter notebook`).

When opening the notebook, the control station first identifies the data stations available. Second it will send the train towards a specific FHIR endpoint (listed in the available data stations), and retrieve the results after the application (train) has been executed.
Third, the control post will send the *same* train towards a specific RDF (SPARQL) endpoint (listed in the available data stations), and retrieve the results of the application after execution.

## Conclusion
This codebase shows that the PHT can be agnostic to the underlying data used. However, as developers of applications/scripts/trains cannot see the actual data, we have to rely on FAIR data descriptions. If FAIR data descriptions are available, applications/trains should be able to interpret these descriptions, and request the data accordingly.
