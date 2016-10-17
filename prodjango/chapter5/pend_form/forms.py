from hashlib import md5

from django import forms

from chapter5.pend_form.models import PendedForm


class PendForm(forms.Form):
    @classmethod
    def get_import_path(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)

    def hash_data(self):
        content = ','.join('%s:%s' % (n, self.data[n]) for n in self.fields.keys())
        return md5(content).hexdigest()

    def pend(self):
        import_path = self.get_import_path()
        form_hash = self.hash_data()
        pended_form = PendedForm.objects.get_or_create(form_class=import_path,
                                                       hash=form_hash)
        for name in self.fields.keys():
            pended_form.data.get_or_create(name=name, value=self.data[name])
        return form_hash

    @classmethod
    def resume(cls, form_hash):
        import_path = cls.get_import_path()
        form = models.PendForm.objects.get(form_class=import_path, hash=form_hash)
        data = dict((d.name, d.value) for d in form.data.all())
        return cls(data)
