import json

import falcon

from . import logger
import recipes
import storage


LOG = logger()


def create_api(middleware):
    app = falcon.API(middleware=middleware)
    app.add_route('/types', TypesResource())
    app.add_route('/types/{by_id}', TypeResource())
    app.add_route('/recipes/manufacturing', RecipeManufacturingResources())
    app.add_route('/recipes/{activity}/{type_id}', ActivityResource())
    return app


def as_int(value):
    try:
        return int(value)
    except ValueError as e:
        LOG.info(e.message)
        return None


def respond_with(found, resp):
    if found:
        resp.body = found
        resp.status = falcon.HTTP_200
    else:
        resp.status = falcon.HTTP_NOT_FOUND


class TypesResource(object):
    @staticmethod
    def on_get(req, resp):
        name_starts = req.get_param('name:starts', default=None)
        result = storage.Type.find(req.context['session'], name_starts)

        found = [row.as_dict() for row in result if row.is_clean()]
        respond_with(json.dumps(found), resp)


class TypeResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        type_id = as_int(by_id)
        if type_id:
            result = storage.Type.get(req.context['session'], type_id)
            if result:
                respond_with(json.dumps(result.as_dict()), resp)
            else:
                resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_400


class ActivityResource(object):
    @staticmethod
    def on_get(req, resp, activity, type_id):
        if activity in recipes.ACTIVITIES:
            lookup = recipes.ACTIVITIES[activity]['func']
            respond_with(lookup(type_id), resp)
        else:
            resp.status = falcon.HTTP_400


class RecipeManufacturingResources(object):
    def on_get(self, req, resp):
        if 'product' in req.params:
            func = recipes.Recipes.prints_making_product
            search_id = req.get_param_as_int('product')
            self.__find_in(func, search_id, resp)
        elif 'material' in req.params:
            # TODO need pagination in this call
            func = recipes.Recipes.prints_using_material
            search_id = req.get_param_as_int('material')
            self.__find_in(func, search_id, resp)
        else:
            raise falcon.HTTPMissingParam(header_name='[material|product]')

    def __find_in(self, func, search_id, resp):
        if search_id:
            print_id = func(search_id)
            if print_id:
                self.__find_resource(recipes.Recipes.manufacturing, print_id, resp)
            else:
                raise falcon.HTTPNotFound()
        else:
            raise falcon.HTTPNotFound()

    @staticmethod
    def __find_resource(func, by_id, resp):
        if by_id.startswith('[') and by_id.endswith(']'):
            accumulator = []
            for n in by_id[1:-1].split(',')[:100]:
                found = func(n.strip())
                if found:
                    accumulator.append(found)
                else:
                    LOG.warning('expected print for [%s] but none found', n)
            found = '[' + ','.join(accumulator) + ']'
        else:
            found = func(by_id)
        respond_with(found, resp)
