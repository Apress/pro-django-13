from django.core import serializers
from django.db.models import AutoField, ForeignKey


field_registry = {}
def serialize_fields(model, fields):
    field_registry[model] = set(fields)


class DataSerializer(serializers.get_serializer('python')):
    def serialize(self, queryset, **options):
        if hasattr(queryset, 'model'):
            model = queryset.model
        else:
            model = queryset[0].__class__

        if options.get('fields', None) is None and model in field_registry:
            options['fields'] = field_registry[model]

        return super(DataSerializer, self).serialize(queryset, **options)

    def get_dump_object(self, obj):
        return self._current

    def handle_fk_field(self, obj, field):
        # Include content from the related object
        related_obj = getattr(obj, field.name)
        value = DataSerializer().serialize([related_obj])
        self._current[field.name] = value[0]

    def get_through_fields(self, obj, field):
        extra = set()

        for f in field.rel.through._meta.fields:
            if isinstance(f, AutoField):
                # Nothing to do with AutoFields, so just ignore it
                continue

            if isinstance(f, ForeignKey):
                # The source will refer to the model of our primary object
                if f.rel.to == obj.__class__:
                    source = f.name
                    continue

                # The target will be the same as on the ManyToManyField
                if f.rel.to == field.rel.to:
                    target = f.name
                    continue

            # Otherwise this is a standard field
            extra.add(f.name)

        return source, target, extra

    def handle_m2m_field(self, obj, field):
        source, target, extra_fields = self.get_through_fields(obj, field)
        fields = field_registry.get(field.rel.to, extra_fields)

        # Find all the relationships for the object passed into this method
        relationships = field.rel.through._default_manager.filter(**{source: obj})

        objects = []
        for relation in relationships.select_related():
            # Serialize the related object first
            related_obj = getattr(relation, target)
            data = DataSerializer().serialize([related_obj])[0]

            # Then add in the relationship data, but only
            # those that were specified in the field list
            for f in fields & extra_fields:
                data[f] = getattr(relation, f)

            objects.append(data)
        self._current[field.name] = objects


class QuerySetSerializer(DataSerializer, serializers.get_serializer('json')):
    pass


class SingleObjectSerializer(QuerySetSerializer):
    def serialize(self, obj, **options):
        # Wrap the object in a list in order to use the standard serializer
        return super(SingleObjectSerializer, self).serialize([obj], **options)

    def getvalue(self):
        # Strip off the outer list for just a single item
        value = super(SingleObjectSerializer, self).getvalue()
        return value.strip('[]\n')
