FROM python:3.5

RUN mkdir precios
COPY . precios/

WORKDIR /precios
RUN pip install -r requirements.txt && ls && chmod 777 start.sh

ENTRYPOINT ["./start.sh"]