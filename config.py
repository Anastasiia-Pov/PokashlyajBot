from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get('TOKEN')
admin_id = os.environ.get('ADMIN_ID')
tg_url = os.environ.get('TG_URL')
git_url = os.environ.get('GIT_URL')
support_chat = os.environ.get('SUPPORT_CHAT')

model_path = os.environ.get('MODEL_PATH')

absolute_path_csvs = os.environ.get('CSV_PATH')
voice_messages_path = os.environ.get('VOICE_PATH')

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
