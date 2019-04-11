# The Google App Engine python runtime is Debian Jessie with Python installed
# and various os-level packages to allow installation of popular Python
# libraries. The source is on github at:
#   https://github.com/GoogleCloudPlatform/python-docker
FROM gcr.io/google-appengine/python

# Create a virtualenv for the application dependencies.
# If you want to use Python 2, add the -p python2.7 flag.
RUN virtualenv -p python3.4 /env

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate. This ensures the application is executed within
# the context of the virtualenv and will have access to its dependencies.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

WORKDIR /app

COPY . ./

# Install dependencies.
RUN pip install -r /app/requirements.txt
