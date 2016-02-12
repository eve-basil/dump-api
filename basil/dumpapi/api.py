import json

import falcon

import recipes
import storage


def create_api(middleware):
    app = falcon.API(middleware=middleware)
    app.add_route('/types', TypesResource())
    app.add_route('/types/{by_id}', TypeResource())
    app.add_route('/recipes/activities', RecipeActivitiesResource())
    app.add_route('/recipes/activities/{by_id}', RecipeActivityResource())
    app.add_route('/recipes/copying/{by_id}', RecipeCopyingResource())
    app.add_route('/recipes/invention/{by_id}', RecipeInventionResource())
    app.add_route('/recipes/manufacturing/{by_id}', RecipeManufacturingResource())
    app.add_route('/recipes/research_material/{by_id}', RecipeResearchMaterialResource())
    app.add_route('/recipes/research_time/{by_id}', RecipeResearchTimeResource())
    return app


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
        result = storage.Type.get(req.context['session'], by_id)

        if result:
            resp.body = json.dumps(result.as_dict())
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404


class RecipeActivitiesResource(object):
    @staticmethod
    def on_get(req, resp):
        resp.body = json.dumps([entry for entry in recipes.ACTIVITIES])
        resp.status = falcon.HTTP_200


class RecipeActivityResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        if by_id in recipes.ACTIVITIES.keys():
            resp.body = json.dumps(recipes.ACTIVITIES[by_id])
            resp.status = falcon.HTTP_200
        resp.status = falcon.HTTP_404


class RecipeCopyingResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        if by_id in recipes.COPYING.keys():
            resp.body = json.dumps(recipes.COPYING[by_id])
            resp.status = falcon.HTTP_200
        resp.status = falcon.HTTP_404


class RecipeInventionResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        if by_id in recipes.INVENTION.keys():
            resp.body = json.dumps(recipes.INVENTION[by_id])
            resp.status = falcon.HTTP_200
        resp.status = falcon.HTTP_404


class RecipeManufacturingResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        if by_id in recipes.MANUFACTURING.keys():
            resp.body = json.dumps(recipes.MANUFACTURING[by_id])
            resp.status = falcon.HTTP_200
        resp.status = falcon.HTTP_404


class RecipeResearchMaterialResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        if by_id in recipes.RESEARCH_MATERIAL.keys():
            resp.body = json.dumps(recipes.RESEARCH_MATERIAL[by_id])
            resp.status = falcon.HTTP_200
        resp.status = falcon.HTTP_404


class RecipeResearchTimeResource(object):
    @staticmethod
    def on_get(req, resp, by_id):
        if by_id in recipes.RESEARCH_TIME.keys():
            resp.body = json.dumps(recipes.RESEARCH_TIME[by_id])
            resp.status = falcon.HTTP_200
        resp.status = falcon.HTTP_404
