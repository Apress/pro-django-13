from django.forms import fields, util


class LatitudeField(fields.DecimalField):
    default_error_messages = {
        'out_of_range': u'Value must be within -90 and 90.',
    }

    def clean(self, value):
        value = super(LatitudeField, self).clean(value)
        if not -90 <= value <= 90:
            raise util.ValidationError(self.error_messages['out_of_range'])
        return value


class LongitudeField(fields.DecimalField):
    default_error_messages = {
        'out_of_range': u'Value must be within -180 and 180.',
    }

    def clean(self, value):
        value = super(LongitudeField, self).clean(value)
        if not -180 <= value <= 180:
            raise util.ValidationError(self.error_messages['out_of_range'])
        return value
