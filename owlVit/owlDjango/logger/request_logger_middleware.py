class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details before processing the request
        self.log_request(request)
        response = self.get_response(request)
        return response

    @staticmethod
    def log_request(request):
        print(f"Method: {request.method}")
        print(f"Path: {request.path}")
        print(f"Body: {request.body.decode('utf-8')}")
        print("-" * 50)

class PortLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the port before processing the request
        self.log_port(request)
        response = self.get_response(request)
        return response

    @staticmethod
    def log_port(request):
        port = request.META['SERVER_PORT']
        print(f"Request came on port: {port}")
