from helper import slack
import datetime

consider_url = ['/api/search', '/api/vectorspace']

class LoggerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        full_url = request.build_absolute_uri()
        if any(u in full_url for u in consider_url):
            ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META['HTTP_USER_AGENT']
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = """
            ```
            [%s]
            url: %s
            ip: %s
            user-agent: %s
            ```""" %(now, full_url,
                    ip, user_agent)
            slack.send_as_thread(msg)
        return self.get_response(request)
