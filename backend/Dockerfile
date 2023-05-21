FROM python:3.10-slim AS todo-backend

ARG PIPX_VERSION=1.2.0
ARG POETRY_VERSION=1.5.0

# Install poetry and set up path
ENV PIPX_BIN_DIR=/opt/pipx/bin
ENV PIPX_HOME=/opt/pipx/home
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH=/opt/pipx/bin:/app/.venv/bin:$PATH

RUN pip install --upgrade pip setuptools
RUN pip install pipx==$PIPX_VERSION
RUN pipx install poetry==$POETRY_VERSION

# Set working directory
WORKDIR /app

# Install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Install todo
COPY todo todo
RUN poetry install

# Copy required project files
COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["bash", "/app/entrypoint.sh"]