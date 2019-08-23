from stat_analyzer.processors.utils import (
    get_max_feature_idx_val,
    max_feature_abs_mean_diff,
)


class DefaultHandler:
    def __init__(self, config):
        self.config = config

    def set_data(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def handle(self):
        getattr(self, 'preprocessing_result')
        getattr(self, 'data')
        data = self.data
        config = self.config
        col_dict = config['col_dict']

        result_dict = {}
        for k, v in col_dict.items():
            if not v:
                continue
            result_dict[k] = v(data, self.preprocessing_result,
                               result_dict=result_dict, config=config)


class ZScalingHandler(DefaultHandler):
    def handle(self):
        getattr(self, 'preprocessing_result')
        getattr(self, 'data')
        config = self.config
        col_dict = config['col_dict']
        standartization_column = config['standartization_column']
        feature_preprocessing_result = self.preprocessing_result
        data = self.data
        result_dict = {}
        data_conversion_func = lambda x: float(config['data_type'](x))

        max_feature_id_key, max_feature_abs_key, dict_remainder =\
            self._get_additional_params(standartization_column, col_dict)

        result_dict[standartization_column] = col_dict[standartization_column](
            data, feature_preprocessing_result, data_conversion_func)
        result_dict[max_feature_id_key], _ =\
            col_dict[max_feature_id_key](result_dict[standartization_column])
        result_dict[max_feature_abs_key] = col_dict[max_feature_abs_key](
            data[result_dict[max_feature_id_key]],
            feature_preprocessing_result['mean'][
                result_dict[max_feature_id_key]],
            data_conversion_func)

        for k in dict_remainder:
            v = col_dict[k]
            if not v:
                continue
            result_dict[k] = v(data, feature_preprocessing_result,
                               result_dict=result_dict, config=config)
        return result_dict

    def _get_additional_params(self, standartization_column, col_dict):
        max_feature_id_key = getattr(self, 'max_feature_id_key', None)
        max_feature_abs_key = getattr(self, 'max_feature_abs_key', None)
        dict_remainder = getattr(self, 'dict_remainder', None)
        if not max_feature_id_key:
            max_feature_id_key = list(col_dict.keys())[
                list(col_dict.values()).index(get_max_feature_idx_val)]
        if not max_feature_abs_key:
            max_feature_abs_key = list(col_dict.keys())[
                list(col_dict.values()).index(max_feature_abs_mean_diff)]
        if not dict_remainder:
            dict_remainder = (set(col_dict.keys()) -
                              set([standartization_column,
                                   max_feature_abs_key,
                                   max_feature_id_key]))
        return max_feature_id_key, max_feature_abs_key, dict_remainder
