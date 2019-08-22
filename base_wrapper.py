from copy import deepcopy

from stat_analyzer.mixins import CheckConfigMixin


class Wrapper(CheckConfigMixin):
    required_fields = {}

    def __init__(self, processors, config={}):
        self._check_config(config)

        self.config = config
        self.processors = []
        for p in processors:
            p.config.update(deepcopy(config))
            self.processors.append(p)

    def compute(self):
        self._compute()

    def _compute(self):
        for processor in self.processors:
            processor.preprocess()
