#docker file for python
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

COPY app/requirements.txt /app/

# install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt
