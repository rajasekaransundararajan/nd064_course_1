FROM python:3.8
LABEL maintainer="Rajasekaran Sundararajan"
# See everything (in a linux container)...
RUN dir -s    
COPY . /app
WORKDIR /app/techtrends

RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "init_db.py"]
CMD [ "python", "app.py" ]