
def z_feature_scaling(data, preprocessing_result, **kwargs):
    values = []
    for i, val in enumerate(data):
        values.append(
            (val - preprocessing_result['mean'][i]) /
            preprocessing_result['std'][i])
    return values


def get_max_feature_idx_val(standardized_results):
    max_val = max(standardized_results)
    idx = standardized_results.index(max_val)

    return idx, max_val


def max_feature_abs_mean_diff(max_val, max_val_idx, mean_for_idx):
    return abs(mean_for_idx - max_val)

