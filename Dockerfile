FROM python:3.10-slim-bullseye
# FROM python:3.10-bullseye

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# COPY ./certs/sg-cert-*.crt /usr/local/share/ca-certificates/
# RUN chmod 644 /usr/local/share/ca-certificates/sg-cert-*.crt && \
#     update-ca-certificates

# RUN echo "[global]" > /etc/pip.conf && \
#     echo "trusted-host = $ARTIF_HOST" >> /etc/pip.conf && \
#     echo "index-url = $ARTIF_GLOBAL_INDEX" >> /etc/pip.conf && \
#     echo "[search]" >> /etc/pip.conf && \
#     echo "index = $ARTIF_SEARCH_INDEX" >> /etc/pip.conf

ENV USER=cors

RUN useradd --create-home $USER && \
    mkdir /app && \
    chown -R $USER:$USER /app

USER $USER

COPY ./conf /app/conf
RUN pip3 install --user --no-cache-dir -r /app/conf/requirements.txt

COPY --chown=$USER:$USER ./certs /app/certs

COPY --chown=$USER:$USER ./bin /app/bin
RUN chmod +x /app/bin/*
# RUN ls -al /app/bin
ENV PATH="/app/bin:${PATH}"

ENV PYTHONPATH=/app/src
COPY ./src /app/src

WORKDIR /app

RUN ls -al /app/bin
RUN ls -al /app/certs
ENTRYPOINT ["/bin/bash", "-c"]

