import redis

from . import logger


LOG = logger()
ACTIVITY_KEYS = ['copying', 'invention', 'manufacturing', 'research_material',
                 'research_time']
RECIPE_STORE = None


class Recipes(object):
    @staticmethod
    def copying(print_id):
        return RECIPE_STORE.get('cop_' + str(print_id))

    @staticmethod
    def invention(print_id):
        return RECIPE_STORE.get('inv_' + str(print_id))

    @staticmethod
    def manufacturing(print_id):
        return RECIPE_STORE.get('man_' + str(print_id))

    @staticmethod
    def research_material(print_id):
        return RECIPE_STORE.get('rem_' + str(print_id))

    @staticmethod
    def research_time(print_id):
        return RECIPE_STORE.get('ret_' + str(print_id))

    @staticmethod
    def prints_making_product(prod_id):
        return RECIPE_STORE.get('byp_' + str(prod_id))

    @staticmethod
    def prints_using_material(mat_id):
        return RECIPE_STORE.get('bym_' + str(mat_id))

ACTIVITIES = {'copying': {'func': Recipes.copying, 'prefix': 'cop_'},
              'invention': {'func': Recipes.invention, 'prefix': 'inv_'},
              'manufacturing': {'func': Recipes.manufacturing, 'prefix': 'man_'},
              'research_material': {'func': Recipes.research_material, 'prefix': 'rem_'},
              'research_time': {'func': Recipes.research_time, 'prefix': 'ret_'},
              }


def bootstrap_store(host, password):
    pool = redis.ConnectionPool(host=host, password=password)
    global RECIPE_STORE
    RECIPE_STORE = redis.StrictRedis(connection_pool=pool)
    return RECIPE_STORE
