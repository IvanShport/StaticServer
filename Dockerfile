FROM python:3.7.4-alpine3.10
WORKDIR /app
COPY . .
EXPOSE 80
CMD ["python", "main.py"]