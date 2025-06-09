# my-blockchain-project/Dockerfile
# Use a slim Python image for smaller size
FROM python:latest-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your blockchain executable into the container
COPY . .

# Install poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the PATH for poetry
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies using poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi
    
# The default command to run your script. This will be overridden by docker-compose for each service.
CMD ["python", "node_exec.py"]
