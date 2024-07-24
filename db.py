from sqlalchemy import create_engine
from sqlmodel import Session
SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:Admin%4023@localhost:3306/ssp_dev"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True  # Log generated SQL
)


def get_session():
    with Session(engine) as session:
        yield session
