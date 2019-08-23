from stat_analyzer.exceptions import ImproperlyConfigured


class CheckConfigMixin:
    @classmethod
    def _check_config(cls, config):
        if not cls.required_fields.issubset(set(config.keys())):
            raise ImproperlyConfigured(
                'The following config fields are mandatory: '
                f'{", ".join(list(cls.required_fields))}'
            )
