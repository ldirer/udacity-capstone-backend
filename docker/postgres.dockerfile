FROM postgres:9.6


ENV POSTGRES_DB "capstone"
ENV POSTGRES_USER "udacity"
ENV POSTGRES_PASSWORD "capstone"

# postgres recommends using a subdirectory of /var/lib/postgresql/data when using a fs mountpoint.
# https://store.docker.com/images/022689bf-dfd8-408f-9e1c-19acac32e57b
ENV PGDATA /var/lib/postgresql/data/pgdata

