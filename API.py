from app import create_app
from app.api.v1.libs.error import APIException, ServerException

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    """
    APIException
    HTTPException
    Exception
    """
    if isinstance(e, APIException):
        return e
    else:
        # 1/0
        if app.config['DEBUG']:
            raise e
        else:
            return ServerException()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
