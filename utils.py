__author__ = 'zhouzhiming'


def check_ip(request):
    if request.remote_ip not in ['127.0.0.1', '10.0.2.2']:
        raise Exception('unauthorized ip')

