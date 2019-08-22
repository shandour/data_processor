from decimal import Decimal

DEFAULT_CONFIG = {
    # the first col in input and output files
    'label_col': None,
    'skip_first': True,
    'delimiter': '\t',
    'data_row_delimiter': ',',
    'data_type': Decimal,
}
