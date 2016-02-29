import json
import os

import yaml
from basil_common import configurables, logger

import recipes as recipes

# TODO rewrite this
LOG = logger()


def collect_activities(blueprint):
    if not isinstance(blueprint, dict):
        raise TypeError(msg='expected blueLOG.info(type dict, found [%s]'
                            % type(blueprint))

    if not isinstance(blueprint['activities'], dict):
        raise TypeError(msg='expected activities dict, found [%s]'
                            % type(blueprint['activities']))
    return [k for k in blueprint['activities'].keys()
            if k in recipes.ACTIVITY_KEYS]


def read_from_file(fn):
    LOG.info('Caching blueprints')
    with open(fn) as f:
        contents = yaml.load(f)

    by_activity = {}
    for activity in recipes.ACTIVITY_KEYS:
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
                    PRINTS_BY_MATERIAL[mat_key] = []
                PRINTS_BY_MATERIAL[mat_key].append(k)


def main():
    configurables.verify(['REDIS_HOST', 'REDIS_PASSWORD'])
    store = recipes.bootstrap_store(host=os.environ['REDIS_HOST'],
                                    password=os.environ['REDIS_PASSWORD'])

    LOG.info('testing redis connection')
    store.info()

    read_from_file(os.environ['BLUEPRINTS_FILE'])

    LOG.info('storing: copying')
    for k, v in COPYING.iteritems():
        store.set('cop_' + str(k), json.dumps(v))

    LOG.info('storing: invention')
    for k, v in INVENTION.iteritems():
        store.set('inv_' + str(k), json.dumps(v))

    LOG.info('storing: manufacturing')
    for k, v in MANUFACTURING.iteritems():
        store.set('man_' + str(k), json.dumps(v))

    LOG.info('storing: material research')
    for k, v in RESEARCH_MATERIAL.iteritems():
        store.set('rem_' + str(k), json.dumps(v))

    LOG.info('storing: time research')
    for k, v in RESEARCH_TIME.iteritems():
        store.set('ret_' + str(k), json.dumps(v))

    LOG.info('storing: prints by product')
    for k, v in PRINTS_BY_PRODUCT.iteritems():
        store.set('byp_' + str(k), json.dumps(v))

    LOG.info('storing: prints by material')
    for k, v in PRINTS_BY_MATERIAL.iteritems():
        store.set('bym_' + str(k), json.dumps(v))

if __name__ == "__main__":
    main()
