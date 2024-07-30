FROM ubuntu:latest
LABEL authors="OneEyeOwl"
ENTRYPOINT ["top", "-b"]

ADD src/main.py .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]

# python:3.10
# docker build -t ollama-medical .
# docker run -p 9999:9999 ollama-medical
# docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# docker pull ollama/ollama