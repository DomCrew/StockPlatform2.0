FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app/collection
COPY collection/finance.py /app/collection

RUN mkdir /app/database
COPY database/database.py database/database_utils.py /app/database/

RUN mkdir /app/database/sql
COPY database/sql /app/database/sql

COPY main.py test.py utils.py /app/

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["sh", "/entrypoint.sh"]