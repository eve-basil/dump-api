import redis

ACTIVITY_KEYS = ['copying', 'invention', 'manufacturing', 'research_material',
                 'research_time']


class Recipes(object):
    def __init__(self, store):
        self._recipes = store

    def activity(self, named):
        return self.__getattribute__(named)

    def copying(self, print_id):
        return self._recipes.get('cop_' + str(print_id))

    def invention(self, print_id):
        return self._recipes.get('inv_' + str(print_id))

    def manufacturing(self, print_id):
        return self._recipes.get('man_' + str(print_id))

    def research_material(self, print_id):
        return self._recipes.get('rem_' + str(print_id))

    def research_time(self, print_id):
        return self._recipes.get('ret_' + str(print_id))

    def prints_making_product(self, prod_id):
        return self._recipes.get('byp_' + str(prod_id))

    def prints_using_material(self, mat_id):
        return self._recipes.get('bym_' + str(mat_id))

    def ping(self):
        return self._recipes.ping()


def bootstrap_store(host, password):
    pool = redis.ConnectionPool(host=host, password=password)
    return redis.StrictRedis(connection_pool=pool)
