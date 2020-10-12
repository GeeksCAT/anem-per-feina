FROM python:3.8
LABEL maintainer="GeeksCAT<info@geekscat.org>"

# build-arg: the name for the non-root user
ARG USR=anemperfeina
# build-arg: the default group of the non-root user
ARG GRP=anemperfeina

WORKDIR /anem-per-feina/

RUN groupadd -r ${GRP} \
    && useradd --no-log-init -r -g ${GRP} ${USR} \
    && chown -R ${USR}:${GRP} /anem-per-feina/

COPY --chown=${USR}:${GRP} requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=${USR}:${GRP} . .

# drop root privileges when running application in container
USER ${USR}

RUN cp .env.dev.sample .env

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]
