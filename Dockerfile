FROM nginx:latest

RUN apt-get update && apt-get install -y \
    software-properties-common
RUN apt-get install -y \
    python3.7 \
    python3-pip

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY /src/config/requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

EXPOSE 80

# command to run on container start
ENTRYPOINT ["python3", "./main.py"] 

