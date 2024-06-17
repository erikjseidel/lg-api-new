FROM python:3.9
WORKDIR /lg-api/app
COPY ./requirements.txt /lg-api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /lg-api/requirements.txt
COPY ./lg-api /lg-api/app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "lg:app"]
