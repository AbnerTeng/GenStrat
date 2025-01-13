FROM python:3.10

WORKDIR /app

COPY ../requirements.txt ./requirements.txt

RUN python -m venv /opt/.venv && /opt/.venv/bin/pip install --upgrade pip
RUN /opt/.venv/bin/pip install -r requirements.txt

ENV PATH="/opt/.venv/bin:$PATH"