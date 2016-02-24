import yaml

from . import logger


LOG = logger()
ACTIVITY_KEYS = ['copying', 'invention', 'manufacturing', 'research_material',
                 'research_time']
ACTIVITIES = None
COPYING = None
INVENTION = None
MANUFACTURING = None
RESEARCH_MATERIAL = None
RESEARCH_TIME = None
PRINTS_BY_PRODUCT = None
PRINTS_BY_MATERIAL = None


def collect_activities(blueprint):
    if not isinstance(blueprint, dict):
        raise TypeError(msg='expected blueprint type dict, found [%s]'
                            % type(blueprint))

    if not isinstance(blueprint['activities'], dict):
        raise TypeError(msg='expected activities dict, found [%s]'
                            % type(blueprint['activities']))
    return [k for k in blueprint['activities'].keys() if k in ACTIVITY_KEYS]


def read_from_file(fn):
    LOG.info('Caching blueprints')
    with open(fn) as f:
        contents = yaml.load(f)

    global ACTIVITIES
    ACTIVITIES = {k: collect_activities(v) for k, v in contents.iteritems()}

    by_activity = {}
    for activity in ACTIVITY_KEYS:
        by_activity[activity] = {k: v['activities'][activity]
                                 for k, v in contents.iteritems()
                                 if activity in v['activities'].keys()}

    global COPYING
    COPYING = by_activity['copying']

    global INVENTION
    INVENTION = by_activity['invention']

    global MANUFACTURING
    MANUFACTURING = by_activity['manufacturing']

    global RESEARCH_MATERIAL
    RESEARCH_MATERIAL = by_activity['research_material']

    global RESEARCH_TIME
    RESEARCH_TIME = by_activity['research_time']

    global PRINTS_BY_PRODUCT
    PRINTS_BY_PRODUCT = {}
    for k, v in MANUFACTURING.iteritems():
        for p in v['products']:
            prod_key = p['typeID']
            PRINTS_BY_PRODUCT[prod_key] = k

    global PRINTS_BY_MATERIAL
    PRINTS_BY_MATERIAL = {}
    for k, v in MANUFACTURING.iteritems():
        if 'materials' in v:
            for m in v['materials']:
                mat_key = m['typeID']
                if mat_key not in PRINTS_BY_MATERIAL:
                    PRINTS_BY_MATERIAL[mat_key] = set()
                PRINTS_BY_MATERIAL[mat_key].add(k)
