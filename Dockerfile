FROM python:3.11
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD app.py .
USER 1337
CMD ["python", "app.py"]
