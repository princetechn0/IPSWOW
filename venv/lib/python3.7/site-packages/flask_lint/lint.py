# -*- coding: utf-8 -*-
from flask import request, current_app
from jsonlint import Json
from jsonlint.meta import DefaultMeta

try:
    from .i18n import translations
except ImportError:
    translations = None  # babel not installed

SUBMIT_METHODS = set(('GET', 'POST', 'PUT', 'PATCH', 'DELETE'))
_Auto = object()


class FlaskLint(Json):
    class Meta(DefaultMeta):
        def wrap_jsondata(self, jsondata, data):
            if data is _Auto:
                if _is_submitted():
                    if request.form:
                        return request.form
                    elif request.get_json():
                        return request.get_json()
                    elif request.args:
                        return request.args

                return None
            return data

        def get_translations(self, data):
            if not current_app.config.get('WTF_I18N_ENABLED', True):
                return None

            return translations

    def __init__(self, jsondata=_Auto, **kwargs):
        super(FlaskLint, self).__init__(jsondata=jsondata, **kwargs)

    def is_submitted(self):
        """
        Consider the submitted if there is an active request and
        the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        """
        return _is_submitted()

    def validate_on_submit(self):
        """
        Call :meth:`validate` only if the data is submitted.
        This is a shortcut for ``lint.is_submitted() and lint.validate()
        """
        return self.is_submitted() and self.validate()


def _is_submitted():
    """Consider the form submitted if there is an active request and
    the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    """
    return bool(request) and request.method in SUBMIT_METHODS
