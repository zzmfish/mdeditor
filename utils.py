__author__ = 'zhouzhiming'


def check_ip(request):
    if request.remote_ip != '127.0.0.1':
        raise Exception('unauthorized ip')

