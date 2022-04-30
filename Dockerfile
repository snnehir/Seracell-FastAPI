FROM python:3.9

WORKDIR /Seracell-FastAPI-Demo

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app","--port=8000", "--host=0.0.0.0", "--reload"]
