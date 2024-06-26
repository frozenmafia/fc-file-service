FROM python:3.10.2

ENV DATABASE_URL="postgresql://postgres:123qwe123qwe@35.238.209.92/postgres"
ENV IAM_SERVICE_URL="https://iam.forge-code.com"
ENV FILE_SERVICE_URL="https://file.forge-code.com"
ENV UPLOADS_DIR="/uploads"
# ENV DATABASE_URL="postgresql://postgres:123qwe123qwe@35.238.209.92/postgres"
# ENV IAM_SERVICE_URL="http://localhost:8001"
# ENV FILE_SERVICE_URL="http://localhost:8004"
# ENV UPLOADS_DIR="/uploads"

WORKDIR /code

RUN python -m venv venv
ENV PATH="/code/venv/bin:$PATH"

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./app /code/app

# Create directories for uploads
RUN mkdir -p $UPLOADS_DIR/images \
    && mkdir -p $UPLOADS_DIR/thumbnails

EXPOSE 8004

# Set the default command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]
