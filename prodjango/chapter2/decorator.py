def optional_arguments_decorator(real_decorator):
    def decorator(func=None, **kwargs):
        # This is the decorator that will be
        # exposed to the rest of your program
        def decorated(func):
            # This returns the final, decorated
            # function, regardless of how it was called
            def wrapper(*a, **kw):
                return real_decorator(func, a, kw, **kwargs)
            return wrapper
        if func is None:
            # The decorator was called with arguments
            def decorator(func):
                return decorated(func)
            return decorator
        # The decorator was called without arguments
        return decorated(func)
    return decorator


if __name__ == '__main__':
    def decorate(func, args, kwargs, prefix='Decorated'):
        return '%s: %s' % (prefix, func(*args, **kwargs))
    decorate = optional_arguments_decorator(decorate)
    
    def test(a, b):
        return a + b
    test = decorate(test)
    
    assert test(13, 17) == 'Decorated: 30'
    test = decorate(test, prefix='Decorated again')
    assert test(13, 17) == 'Decorated again: Decorated: 30'
