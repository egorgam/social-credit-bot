FROM python:3.9
ENV API_TOKEN=${API_TOKEN}
EXPOSE 80
WORKDIR /scb
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app app
COPY store store
CMD ["python", "-m", "app"]
