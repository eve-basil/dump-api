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
    app.add_route('/recipes/activities', RecipeActivitiesResource())
    app.add_route('/recipes/activities/{by_id}', RecipeActivityResource())
    app.add_route('/recipes/copying/{by_id}', RecipeCopyingResource())
    app.add_route('/recipes/invention/{by_id}', RecipeInventionResource())
    app.add_route('/recipes/manufacturing', RecipeManufacturingResources())
    app.add_route('/recipes/manufacturing/{by_id}', RecipeManufacturingResource())
    app.add_route('/recipes/research_material/{by_id}', RecipeResearchMaterialResource())
    app.add_route('/recipes/research_time/{by_id}', RecipeResearchTimeResource())
    return app


def as_int(value):
    try:
        return int(value)
    except ValueError as e:
        LOG.info(e.message)
        return None


def find_resource(resources, by_id, resp):
    type_id = as_int(by_id)
    if type_id:
        if type_id in resources:
            resp.body = json.dumps(resources[type_id])
            resp.status = falcon.HTTP_200
        else:
            raise falcon.HTTPBadRequest()
    else:
        raise falcon.HTTPNotFound()


class TypesResource(object):
    @staticmethod
    def on_get(req, resp):
        name_starts = req.get_param('name:starts', default=None)
        result = storage.Type.find(req.context['session'], name_starts)

        found = [row.as_dict() for row in result if row.is_clean()]
        resp.body = json.dumps(found)
        resp.status = falcon.HTTP_200


class TypeResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        type_id = as_int(by_id)
        if type_id:
            result = storage.Type.get(req.context['session'], type_id)

            if result:
                resp.body = json.dumps(result.as_dict())
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        else:
            resp.status = falcon.HTTP_400


class RecipeActivitiesResource(object):
    @staticmethod
    def on_get(req, resp):
        resp.body = json.dumps([entry for entry in recipes.ACTIVITIES])
        resp.status = falcon.HTTP_200


class RecipeActivityResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        find_resource(recipes.ACTIVITIES, by_id, resp)


class RecipeCopyingResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        find_resource(recipes.COPYING, by_id, resp)


class RecipeInventionResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        find_resource(recipes.INVENTION, by_id, resp)


class RecipeManufacturingResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        find_resource(recipes.MANUFACTURING, by_id, resp)


class RecipeResearchMaterialResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        find_resource(recipes.RESEARCH_MATERIAL, by_id, resp)


class RecipeResearchTimeResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        find_resource(recipes.RESEARCH_TIME, by_id, resp)


class RecipeManufacturingResources(object):
    @staticmethod
    def on_get(req, resp):
        if 'product' in req.params:
            catalog = recipes.PRINTS_BY_PRODUCT
            search_id = req.get_param_as_int('product')
            RecipeManufacturingResources.__find_in(catalog, search_id, resp)
        elif 'material' in req.params:
            catalog = recipes.PRINTS_BY_MATERIAL
            search_id = req.get_param_as_int('material')
            RecipeManufacturingResources.__find_in(catalog, search_id, resp)
        else:
            raise falcon.HTTPMissingParam(header_name='[material|product]')

    @staticmethod
    def __find_in(catalog, search_id, resp):
        if search_id:
            if search_id in catalog:
                print_id = catalog[search_id]
                find_resource(recipes.MANUFACTURING, print_id, resp)
            else:
                raise falcon.HTTPNotFound()
        else:
            raise falcon.HTTPBadRequest()
