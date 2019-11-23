from helper import slack
import datetime

class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_exception(request, exception):
        if not isinstance(exception, SomeExceptionType):
            return None
        return HttpResponse('some message')