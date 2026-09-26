# The access layer as a container: serve.py, the TEXT2SPARQL contract.
# A template for your team's Session 8 stack; not run in class.
# Build from the lab folder:  docker build -f deploy/Dockerfile -t access-layer .
FROM python:3.12-slim
WORKDIR /app
COPY deploy/requirements-access-layer.txt .
RUN pip install --no-cache-dir -r requirements-access-layer.txt
COPY access_layer.py questions_utils.py score_utils.py serve.py examples.ttl void.ttl ./
# Inside the stack the graph is your endpoint, never a file: SPARQL_ENDPOINT is required.
ENV HOST=0.0.0.0 PORT=8000
EXPOSE 8000
CMD ["python", "serve.py"]
