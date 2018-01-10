FROM python:3.6.3
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 80
ENV AWS_ACCESS_KEY_ID 1  
ENV AWS_SECRET_ACCESS_KEY 2  
ENV AWS_SESSION_TOKEN 3
CMD ["python", "main.py"]