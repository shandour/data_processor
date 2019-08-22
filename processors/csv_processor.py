from stat_analyzer.processors.processor_base import Processor
from stat_analyzer.exceptions import ImproperlyConfigured

from typing import List


class CsvProcessor(Processor):
    required_fields = {
        'col_dict',
        'f_format',
        # needed for computations; should also be included in col_dict
        'standartization_column'
    }

    @classmethod
    def _check_config(cls, config):
        super()._check_config(config)
        if config['standartization_column'] not in config['col_dict']:
            raise ImproperlyConfigured(
                'The value of the config standartization_column must '
                'be used as a config col_dict key.'
            )

    def _compute(self, data: List[str], feature):
        config = self.config
        data = [config['data_type'](el) for el in data]

        self.handler.set_data(data=data,
                              preprocessing_result=self.preprocessing_result,
                              feature=feature)

        return self.handler.handle()

