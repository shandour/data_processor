
def z_feature_scaling(data, preprocessing_result, **kwargs):
    values = []
    for i, val in enumerate(data):
        values.append(
            (val - preprocessing_result['mean'][i]) /
            preprocessing_result['std'][i])
    return values


def _get_max_value_helper(result_dict, config):
    standardized_results = result_dict[config['standartization_column']]
    return max(standardized_results)


def get_max_feature_idx(data, preprocessing_result, *,
                        result_dict, config=None):
    return standardized_results.index(_get_max_value_helper(result_dict, config))


def max_feature_abs_mean_diff(data, preprocessing_result, *,
                              result_dict, config=None):
    max_val = _get_max_value_helper(result_dict, config)
    max_val_idx = result_dict[config['standartization_column']].index(max_val)
    idx_mean_val = preprocessing_result['mean'][max_val_idx]

    return abs(idx_mean_val - max_val)

