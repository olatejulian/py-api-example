FROM python:3.11.3-alpine AS builder

RUN pip install -U pip setuptools wheel pdm

WORKDIR /builder

COPY pyproject.toml pdm.lock ./

RUN pdm config python.use_venv false

RUN pdm install --prod --no-editable

FROM python:3.11.3-alpine as production

RUN apk update; apk add -U doas build-base libc6-compat tzdata

ENV TZ=America/Sao_Paulo

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime

ARG CONTAINER_USER_NAME=celery

ARG CONTAINER_USER_GROUP=${CONTAINER_USER_NAME}

RUN addgroup ${CONTAINER_USER_GROUP}

RUN adduser -D ${CONTAINER_USER_NAME} -G wheel ${CONTAINER_USER_GROUP}

RUN echo 'permit nopass :wheel as root' >> /etc/doas.conf

ENV WORKDIR=/home/${CONTAINER_USER_NAME}/app

WORKDIR ${WORKDIR}

RUN chown -R ${CONTAINER_USER_NAME}:${CONTAINER_USER_GROUP} ${WORKDIR}

ENV PYTHONPATH=${WORKDIR}/pkgs/lib

COPY --from=builder /project/__pypackages__/3.10/ ${WORKDIR}/pkgs

COPY src/ src/

RUN touch /var/log/app.log; chown ${CONTAINER_USER_NAME}:${CONTAINER_USER_GROUP} /var/log/app.log

USER ${CONTAINER_USER_NAME}

EXPOSE 5555

CMD ["python", "-m", "celery", "-A", "src.main.celery", "flower"]