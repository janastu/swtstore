

def make_cross_origin_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost'
    response.headers['Access-Control-Max-Age'] = '20days'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,\
                     X-Requested-With, Content-Type, Accept'

    return response
