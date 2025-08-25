# Use Python 3.9.13 base image
FROM python:3.9.13

# Install Rasa version 3.1.7 and additional dependencies
RUN python -m pip install --no-cache-dir rasa==3.1.7 \
    && python -m pip install --no-cache-dir websockets==10.4 PyMySQL

# Set working directory inside the container
WORKDIR /app

# Copy all local files into container at /app
COPY . .

# Use non-root user for security (created by the base image)
USER 1001

# Default entrypoint to call rasa CLI
ENTRYPOINT ["rasa"]

# Default command to run rasa server with API enabled and CORS allowed from all origins, logs output to out.log
CMD ["run", "--enable-api", "--cors", "*", "--log-file", "out.log", "--auth-token", "AnotherSecureRandomString"]

