import json

import falcon

import storage


def start_session(req, resp, resource, params):
    req.context['session'] = storage.Sessions()


def end_session(req, resp, resource):
    req.context['session'].close()


class TypesResource(object):
    @falcon.before(start_session)
    @falcon.after(end_session)
    def on_get(self, req, resp):
        name_starts = req.get_param('name:starts', default=None)
        result = storage.Type.find(req.context['session'], name_starts)

        found = []
        for row in result:
            match = {'id': row.id, 'name': row.name,
                     'volume': row.volume, 'capacity': row.capacity,
                     'portion_size': row.portion_size}
            found.append(match)
        resp.body = json.dumps(found)
        resp.status = falcon.HTTP_200

    @staticmethod
    def select(req):
        return


app = falcon.API()
types = TypesResource()
app.add_route('/types', types)

