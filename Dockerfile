FROM python:3.5

ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt /usr/src/app/
COPY . /usr/src/app/

WORKDIR /usr/src/app
RUN pip install -cache-dir -r requirements.txt

VOLUME ["/usr/src/app"]
EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["./ws.py"]

