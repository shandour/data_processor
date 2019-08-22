import csv
import os.path
import tempfile

from math import sqrt


class CSVPrepocessor:
    def __init__(self, training_data_fpath, features,
                 delimiter, data_type, f_format='csv',
                 data_row_delimiter=',',
                 skip_header=True, count_rows=False):
        self.training_data_fpath = training_data_fpath
        self.features = features
        self.delimiter = delimiter
        self.data_row_delimiter = data_row_delimiter
        self.data_type = data_type
        self.f_format = f_format
        self.skip_header = skip_header
        self.count_rows = count_rows

        self.result_dict = None
        self.tmp_dir = None

    def preprocess(self) -> dict:
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.tmp_dir = tmp_dir
            self._prepare_tmp_files()

            for feature in self.features:
                self._process_feature(feature)

            return self.result_dict

    def _process_feature(self, feature):
        with open(self._get_fpath(feature)) as f:
            self.result_dict[feature] = {
                'mean': {},
                'std': {},
                'row_count': None,
            }

            self._get_means(f, feature, self.count_rows)
            f.seek(0)
            self._get_stds(f, feature)

    def _prepare_tmp_files(self):
        """
         Creates temp files with only those
         rows which have needed features
         with feature values stripped
        """
        training_fpath = self.training_data_fpath
        features = self.features
        delimiter = self.delimiter
        data_row_delimiter = self.data_row_delimiter
        skip_header = self.skip_header

        def handle_line(line, feature_files_dict):
            data_row_line_values = line[1].split(data_row_delimiter)
            data_row_feature = data_row_line_values[0]
            feature_file = feature_files_dict.get(data_row_feature)
            if feature_file:
                feature_file.write(
                    f'{data_row_delimiter}'.join(data_row_line_values[1:]))

        with open(training_fpath) as f:
            try:
                feature_files_dict = {
                    feature: open(self._get_fpath(feature))
                    for feature in features
                }
                csv_reader = csv.reader(f, delimiter=delimiter)
                if skip_header:
                    next(csv_reader)
                for line in csv_reader:
                    handle_line(line, feature_files_dict)
            finally:
                for f in feature_files_dict.values():
                    f.close()

    def _get_fpath(self, feature):
        return os.path.join(self.tmp_dir, f'{feature}.{self.f_format}')

    def _increment_value_and_count(self, feature, attribute, i, value):
        try:
            self.result_dict[feature][attribute][i][0] += value
            self.result_dict[feature][attribute][i][1] += 1
        except KeyError:
            self.result_dict[feature][attribute][i] = (value, 1)

    def _increment_rows(self, feature):
        exists = self.result_dict[feature]['row_count'] is not None
        if exists:
            self.result_dict[feature]['row_count'] += 1
        else:
            self.result_dict[feature]['row_count'] = 1

    def _get_means(self, f, feature, count_rows=False):
        for line in f:
            if count_rows:
                self._increment_rows(feature)
            values = line.split(self.data_row_delimiter)
            for i, val in enumerate(values):
                self._increment_value_and_count(
                    feature, 'mean', i, self.data_type(val.strip()))

            # calculate real value based on Tuple[sum, count]
            for k in self.result_dict[feature]['mean'].keys():
                self.result_dict[feature]['mean'][k] = (
                    self.result_dict[feature]['mean'][k][0] /
                    self.result_dict[feature]['mean'][k][1]
                )

    def _get_stds(self, f, feature, count_rows=False):
        for line in f:
            if count_rows:
                self._increment_rows(feature)
            values = line.split(self.data_row_delimiter)
            for i, val in enumerate(values):
                self._increment_value_and_count(
                    feature, 'std', i,
                    (self.data_type(val.strip()) -
                     self.result_dict[feature]['mean'][i]) ** 2)

            # calculate real value based on Tuple[sum, count]
            for k in self.result_dict[feature]['std'].keys():
                self.result_dict[feature]['std'][k] = sqrt(
                    self.result_dict[feature]['std'][k][0] /
                    self.result_dict[feature]['std'][k][1]
                )

