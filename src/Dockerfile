FROM gcr.io/google_appengine/python
RUN virtualenv -p python3 /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install --upgrade pip && /env/bin/pip install -r /app/requirements.txt
ADD . /app
#RUN /env/bin/python /app/manage.py collectstatic --noinput

CMD gunicorn -b :$PORT main.wsgi
