# pull official base image
FROM python:3.11.4-slim-buster

# Update the package lists for upgrades and new package installations
RUN apt-get update 

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the .env file
COPY .env $HOME/.env

# copy entrypoint.prod.sh
COPY ./entrypoint.prod.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.prod.sh
RUN chmod +x $APP_HOME/entrypoint.prod.sh


# copy project
COPY . $APP_HOME

# run entrypoint.prod.sh
ENTRYPOINT ["sh", "/home/app/web/entrypoint.prod.sh"]
