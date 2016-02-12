import yaml

ACTIVITIES = None

COPYING = None

INVENTION = None

MANUFACTURING = None

RESEARCH_MATERIAL = None

RESEARCH_TIME = None

ACTIVITY_KEYS = ['copying', 'invention', 'manufacturing', 'research_material',
                 'research_time']


def _collect_activities(blueprint):
    if not isinstance(blueprint, dict):
        raise TypeError(msg='expected blueprint type dict, found [%s]'
                            % type(blueprint))

    if not isinstance(blueprint['activities'], dict):
        raise TypeError(msg='expected activities dict, found [%s]'
                            % type(blueprint['activities']))
    return [k for k in blueprint['activities'].keys() if k in ACTIVITY_KEYS]


def read_from_file(fn):
    with open(fn) as f:
        contents = yaml.load(f)

    global ACTIVITIES
    ACTIVITIES = {k: _collect_activities(v) for k, v in contents.iteritems()}

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
