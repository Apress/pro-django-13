from django.core.signing import BadSignature, SignatureExpired


class SignedCookiesMiddleware(object):
    def process_request(self, request):
        for key in request.COOKIES:
            try:
                request.COOKIES[key] = request.get_signed_cookie(key)
            except (BadSignature, SignatureExpired):
                # Invalid cookies should behave as if they were never sent
                del request.COOKIES[key]

    def process_response(self, request, response):
        for (key, morsel) in response.cookies.items():
            print repr(morsel['max-age'])
            if morsel['max-age'] == 0:
                # Deleted cookies don't need to be signed
                continue
            response.set_signed_cookie(key, morsel.value,
                max_age=morsel['max-age'] or None,
                expires=morsel['expires'],
                path=morsel['path'],
                domain=morsel['domain'],
                secure=morsel['secure']
            )
        return response
