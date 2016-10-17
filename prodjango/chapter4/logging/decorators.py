from django.utils.functional import wraps

from chapter4.logging.models import Entry


def logged(view):
    """
    Logs any errors that occurred during the view
    in a special model design for app-specific errors
    """
    def wrapper(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except Exception as e:
            # Log the entry using the application’s Entry model
            Entry.objects.create(path=request.path,
                                 type='View exception',
                                 description=str(e))

            # Re-raise it so standard error handling still applies
            raise
    return wraps(view)(wrapper)
