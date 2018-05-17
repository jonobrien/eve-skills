import os
from flask import Flask, redirect, make_response
from charsheet import CharSheet
from skillcheck import SkillCheck
from flask.views import MethodView


VERSION_1 = '/api/v1'
NO_METHOD = 405




app = Flask(__name__)
app.debug = True  # restart server on edits


def api_error_response(message, errName, code):
    """
    take in message and http error code
    for frontend to have standard responses
    https://github.com/thebigredgeek/apollo-errors

    RETURN apollo-error stylized json
    """
    err = {}
    err['data'] = {}
    err['errors'] = [{
        'message': message,
        'name': errName
    }]
    resp = make_response(json.dumps(err), code)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.errorhandler(NO_METHOD)
def unsupported_method(error):
    """
    globally catch invalid http methods used on any endpoint
    """
    return api_error_response('Endpoint does not support this method',
                              'UnsupportedMethodError', NO_METHOD)


class Login(MethodView):
    """
    redirect to skillsheet
    """
    def get(self):
        resp = make_response(redirect('https://login.eveonline.com/oauth/authorize?response_type=code&redirect_uri=http://localhost:1337/api/v1/skillsheet&client_id=470e0c34a5b340f585f7fe793be9784e&scope=esi-fittings.read_fittings.v1 esi-skills.read_skills.v1'))
        return resp

app.add_url_rule(
    '{0}/login'.format(VERSION_1),
    view_func=Login.as_view('login')
)  # GET


app.add_url_rule(
    '{0}/skillsheet'.format(VERSION_1),
    view_func=CharSheet.as_view('sheet')
)  # GET


app.add_url_rule(
    '{0}/skillcheck/<string:token>'.format(VERSION_1),
    view_func=SkillCheck.as_view('check')
)  # GET








if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)