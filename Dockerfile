FROM python:3.9-slim as builder
ENV PYTHONBUFFERED 1

WORKDIR /app/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.9 as production
WORKDIR /src/
COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
COPY . /src/
EXPOSE 80
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "app.server:app"]