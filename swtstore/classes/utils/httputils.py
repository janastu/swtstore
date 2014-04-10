

def make_cross_origin_headers(response, host_url):
    print 'client\'s host_url: %s' % host_url
    response.headers['Access-Control-Allow-Origin'] = host_url
    response.headers['Access-Control-Max-Age'] = '3600'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'

    print 'Updated headers'
    print response.headers

    return response
