

def z_feature_scaling(data, preprocessing_result,
                      data_conversion_func=lambda x: x):
    values = []
    for i, val in enumerate(data):
        value = data_conversion_func(
            (val - preprocessing_result['mean'][i]) /
            preprocessing_result['std'][i])
        values.append(value)
    return values


def get_max_feature_idx_val(standardized_results):
    max_val = max(standardized_results)
    idx = standardized_results.index(max_val)

    return idx, max_val


def max_feature_abs_mean_diff(max_val, mean_for_idx,
                              data_conversion_func=lambda x: x):
    return data_conversion_func(abs(mean_for_idx - max_val))
