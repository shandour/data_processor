from decimal import Decimal

DEFAULT_CONFIG = {
    # the first col in input and output files
    'label_col': None,
    'skip_header': True,
    'delimiter': '\t',
    'data_row_delimiter': ',',
    'data_type': lambda x: Decimal(x).quantize(Decimal('.000')),
}
