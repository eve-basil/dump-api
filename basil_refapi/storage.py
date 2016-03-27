import json

from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from basil_common import logger


LOG = logger()
Base = declarative_base()


class Region(Base):
    __tablename__ = 'mapRegions'
    id = Column('regionID', Integer, primary_key=True)
    name = Column('regionName', String(100), index=True)
    faction_id = Column('factionID', Integer)

    @staticmethod
    def find(session, prefix=None):
        query = session.query(Region)
        if prefix:
            query = query.filter(Region.name.like(prefix + '%'))

        return query.order_by(Region.name).all()

    @staticmethod
    def get(session, by_id):
        return session.query(Region).filter_by(id=by_id).first()

    def dict(self):
        return {'id': self.id, 'name': self.name,
                'faction_id': self.faction_id}

    def json(self):
        return json.dumps(self.dict())


class SolarSystem(Base):
    __tablename__ = 'mapSolarSystems'
    id = Column('solarSystemID', Integer, primary_key=True)
    name = Column('solarSystemName', String(100), index=True)
    security = Column('security', Float)
    constellation_id = Column('constellationID', Integer, index=True)
    region_id = Column('regionID', Integer, index=True)
    faction_id = Column('factionID', Integer)

    @staticmethod
    def find(session, prefix=None):
        query = session.query(SolarSystem)
        if prefix:
            query = query.filter(SolarSystem.name.like(prefix + '%'))

        return query.order_by(SolarSystem.name).all()

    @staticmethod
    def get(session, by_id):
        return session.query(SolarSystem).filter_by(id=by_id).first()

    def dict(self):
        return {'id': self.id, 'constellation_id': self.constellation_id,
                'name': self.name, 'faction_id': self.faction_id,
                'security': self.security, 'region_id': self.region_id}

    def json(self):
        return json.dumps(self.dict())


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

        return query.order_by(Type.name).all()

    @staticmethod
    def get(session, by_id):
        return session.query(Type).filter_by(id=by_id).first()

    def dict(self):
        return {'id': self.id, 'name': self.name.decode('utf-8', 'replace'),
                'volume': self.volume, 'capacity': self.capacity,
                'portion_size': self.portion_size}

    def json(self):
        try:
            return json.dumps(self.dict())
        except UnicodeDecodeError:
            LOG.warning('UnicodeDecodeError decoding:: id=%s name=%s'
                        % (self.id, self.name))
            return None

# skills = select t.typeID, t.typeName, g.groupName from invTypes as t inner
# join invGroups as g on t.groupID= g.groupID where g.categoryID = 16 and
# t.published = 1 order by g.groupName, typeName;

# select s.stationId, stationName, activityName from staStations s inner join
# ramAssemblyLineStations l on s.stationID = l.stationID inner join
# ramAssemblyLineTypes t on l.assemblyLineTypeID = t.assemblyLineTypeID inner
# join ramActivities a on t.activityID = a.activityID;
