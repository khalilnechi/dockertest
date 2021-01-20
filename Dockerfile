#FROM python:3.5.3
FROM khalilnechi/client_image_ml

WORKDIR /app/

#COPY requirements2.txt main.py __init__.py model.py /app/
COPY app.py model.pkl /app/
#RUN pip install -r ./requirements2.txt
RUN pip install requests
#COPY data/ /app/data
COPY templates/ /app/templates
# ENTRYPOINT /bin/bash
#EXPOSE 5000

#ENV ENVIRONMENT local

ENTRYPOINT python ./app.py
