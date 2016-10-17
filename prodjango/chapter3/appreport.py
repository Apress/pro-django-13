from django.db.models import signals


def app_report(app, created_models, verbosity, **kwargs):
    app_label = app.__name__.split('.')[-2]

    if verbosity == 0:
        # Don't do anything, because the
        # user doesn't want to see this.
        return

    # Get a list of models created for just the current application
    app_models = [m for m in created_models if m._meta.app_label == app_label]

    if app_models:
        # Print a simple status message
        print 'Created %s model%s for %s.' % (len(app_models),
                                              len(app_models) > 1 and 's' or '',
                                              app_label)
        if verbosity == 2:
            # Print more detail about the
            # models that were installed
            for model in app_models:
                print '  %s.%s -> %s' % (app_label,
                                          model._meta.object_name,
                                          model._meta.db_table)

    elif verbosity == 2:
        print '%s had no models created.' % app_label

signals.post_syncdb.connect(app_report)
