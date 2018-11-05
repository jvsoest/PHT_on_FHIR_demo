FROM python:3.7

COPY requirements.txt /requirements.txt
COPY run.py /run.py
COPY sparql.py /sparql.py
COPY fhir.py /fhir.py

RUN pip install -r requirements.txt

CMD ["python", "run.py"]