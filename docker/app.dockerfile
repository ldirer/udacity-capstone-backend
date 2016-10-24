FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip

# This does not work, the aliases are created... For the shell that closes after the RUN command.
# RUN alias pip="/usr/bin/pip3" && alias python="/usr/bin/python3"
ENV PATH="/usr/bin/pip3:/usr/bin/python3:$PATH"

RUN pip3 install --upgrade pip setuptools

RUN mkdir udacity_capstone
WORKDIR udacity_capstone

COPY requirements.txt /udacity_capstone

# Required for psycopg2
RUN apt-get install -y postgresql-common libpq-dev

RUN /usr/bin/pip3 install -r requirements.txt

COPY / /udacity_capstone

# The docs:
# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime.
# EXPOSE does not make the ports of the container accessible to the host

# So that's BS.
# EXPOSE 5000:5000

# Yeah, I still need to debug some stuff...
RUN apt-get install -y vim

# MUAHAHA dont forget the host part...
# Otherwise it listens *only* to localhost, and you know how your docker host localhost ain't your docker localhost...
# Development command.
# CMD python3 manage.py runserver -h 0.0.0.0

CMD uwsgi uwsgi.ini

