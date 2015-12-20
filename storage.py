import os
import sys

from sqlalchemy import create_engine
from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Type(Base):
    __tablename__ = 'invTypes'
    id = Column('typeID', Integer, primary_key=True)
    group_id = Column('groupID', Integer)
    name = Column('typeName', String(100))
    volume = Column(Float)
    capacity = Column(Float)
    base_price = Column('basePrice', Float)
    market_group_id = Column('marketGroupID', Integer)
    portion_size = Column('portionSize', Integer)
    published = Column(Boolean)

    @staticmethod
    def find(session, prefix=None):
        query = session.query(Type).filter_by(published=True)
        if prefix:
            query = query.filter(Type.name.like(prefix + '%'))

        return query.all()

if not os.environ.get('DB_USER', None):
    sys.stderr.write('DB_USER not set in environment')
    os.exit(1)
if not os.environ.get('DB_PASS', None):
    sys.stderr.write('DB_PASS not set in environment')
    os.exit(1)
if not os.environ.get('DB_HOST', None):
    sys.stderr.write('DB_HOST not set in environment')
    os.exit(1)
if not os.environ.get('DB_NAME', None):
    sys.stderr.write('DB_NAME not set in environment')
    os.exit(1)

db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']

connect_str = 'mysql://%s:%s@%s/%s' % (db_user, db_pass, db_host, db_name)
engine = create_engine(connect_str, echo=True)
Sessions = sessionmaker(bind=engine)