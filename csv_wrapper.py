import csv
from copy import deepcopy
import os.path

from stat_analyzer.defaults import DEFAULT_CONFIG
from stat_analyzer.base_wrapper import Wrapper


class CsvWrapper(Wrapper):
    required_fields = {
        'features',
        'training_data_fpath',
        'input_fpath',
        'output_fpath',
        'delimiter',
        'data_row_delimiter',
        'skip_header',
        'data_type',
        'label_col',
    }

    def __init__(self, processors, config={}):
        merged_conf = deepcopy(DEFAULT_CONFIG)
        merged_conf.update(config)
        super().__init__(processors, merged_conf)

    def _compute(self):
        super()._compute()
        config = self.config
        label_col = config['label_col']
        delimiter = config['delimiter']
        features = config['features']
        input_fpath = config['input_fpath']
        output_fpath = config['output_fpath']
        skip_first = config['skip_first']
        data_row_delimiter = config['data_row_delimiter']

        with open(input_fpath) as input_file:
            fieldnames = [label_col]
            for p in self.processors:
                fieldnames.extend(p.col_names)

            for feature in features:
                input_file.seek(0)
                fpath = self._get_output_fname(output_fpath, feature)
                with open(fpath, 'w') as output_file:
                    writer = csv.DictWriter(
                        output_file,
                        delimiter=delimiter,
                        fieldnames=fieldnames)
                    writer.writeheader()
                    if skip_first:
                        input_file.readline()
                    for line in input_file:
                        identifier, data = line.split(delimiter)
                        line_dict = {label_col: identifier}
                        for processor in self.processors:
                            line_dict.update(
                                processor.compute(
                                    data[1:].split(data_row_delimiter),
                                    feature))
                        writer.writerow(line_dict)

    @staticmethod
    def _get_output_fname(output_fpath, feature):
        head, tail = os.path.split(output_fpath)
        return f'{head + "/" if head else ""}{feature}_{tail}'
