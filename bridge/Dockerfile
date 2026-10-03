FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bridge.py security.py .
ENV OLLAMA_URL=http://host.docker.internal:11434
ENV BRIDGE_API_KEY=
ENV LOG_LEVEL=INFO
EXPOSE 5000
CMD ["python", "bridge.py"]
