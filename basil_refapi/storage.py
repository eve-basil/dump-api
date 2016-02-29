import json

from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from basil_common import logger


LOG = logger()
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

    @staticmethod
    def get(session, by_id):
        return session.query(Type).filter_by(id=by_id).first()

    def as_dict(self):
        return {'id': self.id, 'name': self.name.decode('utf-8', 'replace'),
                'volume': self.volume, 'capacity': self.capacity,
                'portion_size': self.portion_size}

    def is_clean(self):
        try:
            json.dumps({'name': self.name})
        except UnicodeDecodeError:
            LOG.warning('UnicodeDecodeError decoding:: id=%s name=%s'
                        % (self.id, self.name))
            return False
        else:
            return True

# skills = select t.typeID, t.typeName, g.groupName from invTypes as t inner
# join invGroups as g on t.groupID= g.groupID where g.categoryID = 16 and
# t.published = 1 order by g.groupName, typeName;
