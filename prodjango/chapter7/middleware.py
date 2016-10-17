class MinimumResponseMiddleware(object):
    """
    Makes sure a response is at least a certain size
    """
    def __init__(self, min_length=1024):
        self.min_length = min_length

    def process_response(self, request, response):
        """
        Pads the response content to be at least as
        long as the length specified in __init__()
        """
        response.content = response.content.ljust(self.min_length)
