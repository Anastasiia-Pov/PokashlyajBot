FROM python:3.11.9
WORKDIR /PokaschlyajBot
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get -y update && apt-get install -y libsndfile1

RUN mkdir -p /PokaschlyajBot/voice_messages
RUN mkdir -p /PokaschlyajBot/csvs_saved
RUN chmod 755 .

COPY . .

CMD ["python", "main.py"]

# RUN apt-get install sqlite3
# RUN sqlite3 users.db.sqlite3
