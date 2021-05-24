FROM python:slim

WORKDIR /flask_web

ADD . /flask_web

RUN pip install -r requirements.txt

CMD ["python3","AccessLog.py"]

