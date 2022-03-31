FROM tiangolo/uwsgi-nginx-flask

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN pip install -U pip
RUN pip install setuptools wheel

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

ENV CONFIG_NAME=DevelopmentConfig

COPY entrypoint.sh /var/entrypoint.sh
RUN chmod +x /var/entrypoint.sh
ENTRYPOINT ["/var/entrypoint.sh"]

CMD python app.py

EXPOSE 5000