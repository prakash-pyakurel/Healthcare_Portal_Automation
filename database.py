from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite connection (this is a local file-based DB)
DATABASE_URL = "sqlite:///./claims_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String)
    name = Column(String)
    service_date = Column(String)
    billing_code = Column(String)


# Create the database table
Base.metadata.create_all(bind=engine)
