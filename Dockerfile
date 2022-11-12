FROM python:3.9.7

WORKDIR /user/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicron", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
