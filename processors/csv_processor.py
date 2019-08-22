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
        col_dict = config['col_dict']
        data = [config['data_type'](el) for el in data]

        result_dict = {}
        for k, v in col_dict.items():
            if not v:
                continue
            result_dict[k] = v(data, self.preprocessing_result[feature],
                               result_dict=result_dict, config=config)
