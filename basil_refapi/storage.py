import json

from sqlalchemy import Column, Float, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from basil_common import logging

LOG = logging.getLogger(__name__)
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
        return session.query(Region).get(by_id)

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
        return session.query(SolarSystem).get(by_id)

    def dict(self):
        return {'id': self.id, 'constellation_id': self.constellation_id,
                'name': self.name, 'faction_id': self.faction_id,
                'security': self.security, 'region_id': self.region_id}

    def json(self):
        return json.dumps(self.dict())


class Station(Base):
    __activities = {1: 'Manufacturing', 3: 'Researching Time Efficiency',
                    4: 'Researching Material Efficiency', 5: 'Copying',
                    7: 'Reverse Engineering', 8: 'Invention'}
    __tablename__ = 'staStations'
    id = Column('stationID', Integer, primary_key=True)
    name = Column('stationName', String(100), index=True)
    region_id = Column('regionID', Integer)
    constellation_id = Column('constellationID', Integer)
    system_id = Column('solarSystemID', Integer)
    owning_corp = Column('corporationID', Integer)
    office_rental = Column('officeRentalCost', Integer)
    reprocessing_efficiency = Column('reprocessingEfficiency', Float)
    _session = None

    # TODO activities_available via ramAssemblyLineStations and activities
    @staticmethod
    def find(session, prefix=None):
        query = session.query(Station)
        if prefix:
            query = query.filter(Station.name.like(prefix + '%'))

        found = query.order_by(Station.name).all()
        for station in found:
            station._session = session
        return found

    @staticmethod
    def get(session, by_id):
        found = session.query(Station).get(by_id)
        if found:
            found._session = session
        return found

    def dict(self):
        return {'id': self.id, 'constellation_id': self.constellation_id,
                'system_id': self.system_id, 'system_name': self.system_name,
                'region_name': self.region_name, 'name': self.name,
                'region_id': self.region_id, 'owning_corp': self.owning_corp,
                'reprocessing_efficiency': self.reprocessing_efficiency,
                'office_rental': self.office_rental}

    def json(self):
        return json.dumps(self.dict())

    @property
    def region_name(self):
        return Region.get(self._session, self.region_id).name

    @property
    def system_name(self):
        # 30004712
        return SolarSystem.get(self._session, self.system_id).name


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

    meta_level = None
    _meta_level_attrib_query = ("select attributeID from dgmAttributeTypes "
                                "where attributeName = 'metaLevel';")
    _meta_lvl_query = ("select valueInt from dgmTypeAttributes "
                       "where typeID = %s and attributeID = %s")

    @staticmethod
    def initialize(engine):
        result = engine.execute(Type._meta_level_attrib_query)
        for row in result:
            Type.meta_level = row[0]

    @staticmethod
    def find(session, prefix=None):
        query = session.query(Type).filter_by(published=True)
        if prefix:
            query = query.filter(Type.name.like(prefix + '%'))

        type_instances = query.order_by(Type.name).all()
        for instance in type_instances:
            instance.add_meta_level(session)
        return type_instances

    @staticmethod
    def get(session, by_id):
        instance = session.query(Type).get(by_id)
        if instance:
            instance.add_meta_level(session)
        return instance

    def add_meta_level(self, session):
        query = Type._meta_lvl_query % (self.id, Type.meta_level)
        result = session.execute(query).first()
        if result:
            self.meta_level = result[0]

    def dict(self):
        return {'id': self.id, 'name': self.name.decode('utf-8', 'replace'),
                'volume': self.volume, 'capacity': self.capacity,
                'meta': self.meta_level, 'portion_size': self.portion_size}

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
