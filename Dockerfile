FROM python:3

ADD proj.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./proj.py"]
