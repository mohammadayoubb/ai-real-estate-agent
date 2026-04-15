FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


  #"query": "A 1-story house with 1800 square feet of living space, 3 bedrooms, and 2 full bathrooms. The house has an overall quality rating of 6, includes a 2-car garage, and sits on a 8000 square foot lot. Built in 2005 and located in the CollgCr neighborhood. Total of 7 rooms."
  #A small single-story house with 900 square feet of living space, 2 bedrooms, and 1 bathroom. The house has an overall quality rating of 4, no garage, and sits on a 5000 square foot lot. Built in 1970 and located in the OldTown neighborhood. Total of 4 rooms.