from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')

db_connection_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}?charset=utf8mb4"
engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)