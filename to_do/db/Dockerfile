# Use an official PostgreSQL image as the base image
FROM postgres:17

# Set the password for the postgres user
ENV POSTGRES_PASSWORD=mysecretpassword

# Expose the PostgreSQL port
EXPOSE 5432

# Run the PostgreSQL database
CMD ["psql -U postgres"]