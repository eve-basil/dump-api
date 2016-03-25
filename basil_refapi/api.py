import json

import falcon
from basil_common import list_support as lists, logger, str_support as strs

import recipes
from storage import Type


LOG = logger()


# TODO create common caching/headers middleware, see also
# https://svn.tools.ietf.org/svn/wg/httpbis/draft-ietf-httpbis/
# latest/p2-semantics.html

def create_api(middleware):
    app = falcon.API(middleware=middleware)
    app.add_route('/health', HealthResource())
    app.add_route('/types', TypesResource())
    app.add_route('/types/{by_id}', TypeResource())
    app.add_route('/recipes/{activity}/{type_id}', ActivityResource())
    # NOTE Doesn't use recipes b/c of
    # https://github.com/falconry/falcon/issues/702
    app.add_route('/recipe/manufacturing', RecipeSearchResource())
    return app


def respond_with(found, resp):
    if found:
        resp.body = found
        resp.status = falcon.HTTP_200
    else:
        resp.status = falcon.HTTP_NOT_FOUND


class HealthResource(object):
    @staticmethod
    def on_get(req, resp):
        respond_with('{"status": "ok"}')


class TypesResource(object):
    @staticmethod
    def on_get(req, resp):
        name_starts = req.get_param('name:starts', default=None)
        result = Type.find(req.context['session'], name_starts)

        found = [row.dict() for row in result if row.is_clean()]
        respond_with(json.dumps(found), resp)


class TypeResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        type_id = strs.as_int(by_id)
        if type_id:
            result = Type.get(req.context['session'], type_id)
            if result:
                respond_with(result.json(), resp)
            else:
                raise falcon.HTTPNotFound
        else:
            raise falcon.HTTPBadRequest('Invalid ID',
                                        'Expected integer identifier')


class ActivityResource(object):
    @staticmethod
    def on_get(req, resp, activity, type_id):
        if activity in recipes.ACTIVITY_KEYS:
            recipe_store = req.context['recipes']
            lookup = recipe_store.activity(activity)
            respond_with(lookup(type_id), resp)
        else:
            raise falcon.HTTPNotFound


class ManufResource(object):
    @staticmethod
    def on_get(req, resp, type_id):
        recipe_store = req.context['recipes']
        lookup = recipe_store.activity('manufacturing')
        respond_with(lookup(type_id), resp)


class RecipeSearchResource(object):
    def on_get(self, req, resp):
        recipe_store = req.context['recipes']
        if 'product' in req.params:
            func = recipe_store.prints_making_product
            search_id = req.get_param_as_int('product')
            self.__find_in(func, search_id, recipe_store, resp)
        elif 'material' in req.params:
            # TODO should add pagination in this call
            # maybe like https://github.com/etalab/ban/blob/master/ban/http
            # /resources.py#L45
            func = recipe_store.prints_using_material
            search_id = req.get_param_as_int('material')
            self.__find_in(func, search_id, recipe_store, resp)
        else:
            raise falcon.HTTPMissingParam('material" or "product')

    def __find_in(self, func, search, store, resp):
        if search:
            search_key = func(search)
            if search_key:
                self.__find_resource(store.manufacturing, search_key, resp)
                return

        raise falcon.HTTPNotFound()

    @staticmethod
    def __find_resource(func, param, resp):
        if lists.is_list_like(param):
            limited_matches = lists.list_from_str(param)
            matches = [func(n.strip()) for n in limited_matches
                       if func(n.strip())]
            found = '[' + ','.join(matches) + ']'
        else:
            found = func(param)
        respond_with(found, resp)
