from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import os
from pathlib import Path
import dotenv
import logging

dotenv.load_dotenv()

db_url = os.environ.get('POSTGRES_URL')
#engine = create_engine(db_url, connect_args={'check_same_thread': False})
engine = create_engine(db_url)

# Make the engine
#engine = create_engine(db_url, future=True, echo=True,
#                       connect_args={"check_same_thread": False})

from typing import Generator
from sqlalchemy.orm import Session

LocalSession = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

def init_paths() -> None:
    log_dir = os.environ.get('LOG_DIR')
    log_file = os.environ.get('LOG_FILE')

    if log_dir is not None:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
    if log_file is not None:
        logging.basicConfig(filename=log_file)


init_paths()