import functools
import http


def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, the function returns a 401 error
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        current_user = self.get_current_user()
        if not current_user:
            raise Exception(http.HTTPStatus.UNAUTHORIZED, 401, "Unauthorized.")

        return method(self, *args, **kwargs)

    return wrapper
