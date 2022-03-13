FROM python:3.9

WORKDIR /seracell_fastapi

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app","--port=8000", "--host=0.0.0.0", "--reload"]
