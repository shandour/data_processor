from copy import deepcopy
from stat_analyzer.mixins import CheckConfigMixin
from stat_analyzer.processors.handlers import DefaultHandler


class Processor(CheckConfigMixin):
    # col_dict contains key-value pairs [col_name]: [evaluation_function]
    required_fields = {'col_dict', 'f_format'}

    def __init__(self, preprocessor_cls, handler=DefaultHandler,
                 config={}, delayed=False):
        self.config = config
        self._initialized = not delayed
        self.preprocessor = preprocessor_cls
        self.handler = handler(config)
        self.preprocessing_result = None

        if not delayed:
            self._init_preprocessor()

    def _init_preprocessor(self):
        self.preprocessor = self.preprocessor(deepcopy(self.config))

    @property
    def col_names(self):
        return self.config['col_dict'].keys()

    def compute(self, *args, config={}, **kwargs):
        self.config.update(config)
        self._check_config(self.config)
        if not self._initialized:
            self._init_preprocessor()
        self._compute(*args, **kwargs)

    def _compute(self, *args, **kwargs):
        raise NotImplemented

    def preprocess(self, *, config={}):
        self.config.update(config)
        if not self._initialized:
            self._init_preprocessor()
        self.preprocessing_result = self.preprocessor.preprocess()

