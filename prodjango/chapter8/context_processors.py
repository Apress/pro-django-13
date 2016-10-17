def remote_addr(request):
    return {'ip_address': request.META['REMOTE_ADDR']}
