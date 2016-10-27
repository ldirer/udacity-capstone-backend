FROM postgres:9.6


ENV POSTGRES_DB "capstone"
ENV POSTGRES_USER "udacity"
ENV POSTGRES_PASSWORD "capstone"

# postgres recommends using a subdirectory and not setting PGDATA directly to a fs mountpoint.
# https://store.docker.com/images/022689bf-dfd8-408f-9e1c-19acac32e57b
# This assumes we mounted our persistent disk at /var/lib/postgresql/data

# Fun fact: I think this RUN mkdir happens *before* our mounted volume is created, so it also creates the pgdata
# directory on the host directory associated with the volume created by the base postgres image.
# Basically we get `pgdata` as output from the command:
# sudo ls /var/lib/docker/volumes/97197d0009b54077c9a56b0ab1dbb2034aaa41bc311c37061a1c084931d1f703/_data/
RUN mkdir -p /var/lib/postgresql/data/pgdata
ENV PGDATA /var/lib/postgresql/data/pgdata

