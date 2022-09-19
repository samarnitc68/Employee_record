FROM python:3.8

WORKDIR /flask-Employee

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY ./emp ./emp

CMD ["python", "./emp/employee.py"]