From python:3.9.7

WORKDIR /user/src/app

COPY requirements.txt ./
#COPY requirements.txt /user/scr/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicron", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
