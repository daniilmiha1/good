from sqlalchemy import Column, BigInteger, CHAR, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__: str = "users"

    id = Column(BigInteger, primary_key=True)
    locale = Column(CHAR(2), ForeignKey('languages.name'), nullable=False)
    is_blocked = Column(Boolean, default=False)


class Language(Base):
    __tablename__: str = "languages"

    name = Column(CHAR(2), primary_key=True)
