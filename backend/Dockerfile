FROM python:3.4-alpine
ADD . /var/code
WORKDIR /var/code
EXPOSE 5000
RUN apk update
RUN apk add gcc musl-dev gmp-dev mpfr-dev mpc1-dev
RUN pip install flask flask-socketio flask-cors eventlet pymongo gmpy2
#RUN pip install -r requirements.txt
CMD python backend_service.py
