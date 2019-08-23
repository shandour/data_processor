a working example how a resultant file for feature '2' can be generated:

from stat_analyzer.csv_wrapper import CsvWrapper
from stat_analyzer.processors import CsvProcessor, ZScalingHandler
from stat_analyzer.preprocessors import CsvPrepocessor
from stat_analyzer.processors.utils import (
  z_feature_scaling,
  get_max_feature_idx_val,
  max_feature_abs_mean_diff,
)


processor_config = {
        'col_dict': {
            'feature_stand': z_feature_scaling,
            'feature_max_idx': get_max_feature_idx_val,
            'feature_max_abs_diff': max_feature_abs_mean_diff,
        },
        'f_format': 'tsv',
        'standartization_column': 'feature_stand',
}

pr = CsvProcessor(CsvPrepocessor, handler=ZScalingHandler, config=processor_config)

wrapper_config = {
  'features': ['2'],
  'input_fpath': './data/input.tsv', 
  'output_fpath': './data/output.tsv',
  'training_data_fpath': './data/training_data.tsv',
  'label_col': 'id_job',
}

processors = [pr]
w = CsvWrapper(processors, wrapper_config)
w.compute()


Preprocessors prepare data for processors. Processors are called from within their respective wrapper. For each feature a file named {feature}_{your output_path_file_name}.{file_format} is generated.
