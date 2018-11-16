FROM python

COPY ./code /code
WORKDIR /code
#RUN apt-get update
#RUN apt-get install -y libpq-dev
RUN pip install -r requirements.txt

CMD python run.py