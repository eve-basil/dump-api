import json

import falcon

import storage


def create_api(middleware):
    app = falcon.API(middleware=middleware)
    types = TypesResource()
    type_by_id = TypeResource()
    app.add_route('/types', types)
    app.add_route('/types/{by_id}', type_by_id)
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
