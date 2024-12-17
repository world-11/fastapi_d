from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Создаем движок базы данных
engine = create_engine(
    "sqlite:///database.db", connect_args={"check_same_thread": False}
)


class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    def __repr__(self):
        return f"Athlete(id={self.id}, name={self.name}, age={self.age})"


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    date = Column(String)

    def __repr__(self):
        return f"Competition(id={self.id}, title={self.title}, date={self.date})"


class Participation(Base):
    __tablename__ = "participation"

    athlete_id = Column(Integer, ForeignKey("athletes.id"), primary_key=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"), primary_key=True)
    athlete = relationship(Athlete)
    competition = relationship(Competition)

    def __repr__(self):
        return f"Participation(athlete_id={self.athlete_id}, competition_id={self.competition_id})"


# Создаем таблицы в базе данных
Base.metadata.create_all(engine)


# Создаем сессию для взаимодействия с базой данных
SessionLocal = sessionmaker(bind=engine, autoflush=False)
