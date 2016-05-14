import json
import logging

import falcon
from basil_common import list_support as lists, str_support as strs
from basil_common.falcon_support import respond

import recipes
from storage import Region, SolarSystem, Station, Type


LOG = logging.getLogger(__name__)


# TODO create common caching/headers middleware, see also
# https://svn.tools.ietf.org/svn/wg/httpbis/specs/rfc7231.html

def create_api(middleware):
    app = falcon.API(middleware=middleware)
    app.add_route('/health', HealthResource())
    app.add_route('/recipes/{activity}/{type_id}', ActivityResource())
    # NOTE Doesn't use recipes b/c of
    # https://github.com/falconry/falcon/issues/702
    app.add_route('/recipe/manufacturing', RecipeSearchResource())
    app.add_route('/regions', StorageResources(Region))
    app.add_route('/regions/{by_id}', StorageResource(Region))
    app.add_route('/stations', StorageResources(Station))
    app.add_route('/stations/{by_id}', StorageResource(Station))
    app.add_route('/systems', StorageResources(SolarSystem))
    app.add_route('/systems/{by_id}', StorageResource(SolarSystem))
    app.add_route('/types', StorageResources(Type))
    app.add_route('/types/{by_id}', StorageResource(Type))
    return app


class HealthResource(object):
    """Provides a health check endpoint

       Ensures the service is running and accessing the data sources expected.
    """
    @staticmethod
    def on_get(req, resp):
        pong = req.context['recipes'].ping()
        record = req.context['session'].query(Type).first()
        if pong and record:
            respond(resp, body='{"status": "ok"}')
        raise falcon.HTTPInternalServerError('Service Unavailable.', None)


class StorageResources(object):
    """Provides read-only access to lists of resources from DB Storage.

       Any type from Storage, and thus from the DB can be specified as a
       resource_type to the StorageResources constructor to allow common
       GET query operation.
    """
    def __init__(self, resource_type):
        self._db_type = resource_type

    def on_get(self, req, resp):
        name_starts = req.get_param('name:starts', default=None)
        result = self._db_type.find(req.context['session'], name_starts)

        found = [row.dict() for row in result]
        respond(resp, body=json.dumps(found))


class StorageResource(object):
    """Provides read-only access to resources from DB Storage.

       Any type from Storage, and thus from the DB can be specified as a
       resource_type to the StorageResources constructor to allow a GET.
    """
    def __init__(self, resource_type):
        self._db_type = resource_type

    def on_get(self, req, resp, by_id):
        resource_id = strs.as_int(by_id)
        if not resource_id:
            raise falcon.HTTPBadRequest('Invalid ID',
                                        'Expected integer identifier')

        result = self._db_type.get(req.context['session'], resource_id)
        if result:
            respond(resp, body=result.json())
        else:
            respond(resp, status=falcon.HTTP_NOT_FOUND)


class ActivityResource(object):
    """Provides read-only access to blueprint recipes, organized by activity.
    """
    @staticmethod
    def on_get(req, resp, activity, type_id):
        if activity in recipes.ACTIVITY_KEYS:
            recipe_store = req.context['recipes']
            activity_lookup = recipe_store.activity(activity)
            respond(resp, body=activity_lookup(type_id))
        else:
            respond(resp, status=falcon.HTTP_NOT_FOUND)


class RecipeSearchResource(object):
    """Provides read-only searching for blueprint manufacture recipes.

       Searches can be by product or by material.
    """
    def on_get(self, req, resp):
        recipe_store = req.context['recipes']
        if 'product' in req.params:
            func = recipe_store.prints_making_product
            search_id = req.get_param_as_int('product')
            self.__find_in(func, search_id, recipe_store, resp)
        elif 'material' in req.params:
            func = recipe_store.prints_using_material
            search_id = req.get_param_as_int('material')
            self.__find_in(func, search_id, recipe_store, resp)
        else:
            raise falcon.HTTPMissingParam('"material" or "product"')

    def __find_in(self, func, search, store, resp):
        if search:
            search_key = store.manufacturing(search)
            if search_key:
                if lists.is_list_like(search_key):
                    limited_matches = lists.list_from_str(search_key)
                    matches = [func(n.strip()) for n in limited_matches
                               if func(n.strip())]
                    found = '[' + ','.join(matches) + ']'
                else:
                    found = store.manufacturing(search_key)
                respond(resp, body=found)
                self.__find_resource(store.manufacturing, search_key, resp)
                return

        raise falcon.HTTPNotFound()
