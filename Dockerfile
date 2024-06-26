FROM python:3.10.7-buster as python-base

ARG STAGE
ARG DEBUG
ARG TIMEZONE_OFFSET

ENV STAGE=${STAGE}
ENV DEBUG=${DEBUG}
ENV TIMEZONE_OFFSET=${TIMEZONE_OFFSET}
ENV PYTHONUNBUFFERED=1

# Poetry environment
ENV POETRY_VERSION=1.4.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base

# Install Poetry
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as app

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . .

# Install dependencies
RUN poetry check
RUN poetry config virtualenvs.in-project false
RUN poetry install $(if [ "$STAGE" = 'production' ]; then echo '--without dev'; fi) --no-interaction --no-cache

# Expose the port that Uvicorn will listen on
EXPOSE 8000

# Run Uvicorn in production mode
CMD ["poetry", "run", "uvicorn", "aftercurrency.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
