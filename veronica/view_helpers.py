import flask


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers['content-type'] = 'text/xml'
    return resp
