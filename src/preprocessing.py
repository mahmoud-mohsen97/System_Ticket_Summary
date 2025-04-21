import pandas as pd


def load_raw_data(file_obj, delimiter=','):
    """
    Read a raw ticket data text file into a pandas DataFrame.
    Tries the specified delimiter (default comma), then falls back to tab if parsing fails.

    Parameters:
        file_obj: file-like object or file path
        delimiter: str, initial delimiter to use for parsing

    Returns:
        pd.DataFrame
    """
    try:
        df = pd.read_csv(file_obj, sep=delimiter, dtype=str)
    except pd.errors.ParserError:
        df = pd.read_csv(file_obj, sep='\t', dtype=str)
    return df


def parse_dates(df, date_cols, date_format="%m/%d/%Y %H:%M"):
    """
    Convert specified columns in a DataFrame to datetime.

    Parameters:
        df: pd.DataFrame
        date_cols: list of str, column names to parse as datetime
        date_format: str, format specifier for parsing

    Returns:
        pd.DataFrame with converted datetime columns
    """
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], format=date_format, errors='coerce')
    return df


def filter_by_category(df, category_col, categories):
    """
    Filter DataFrame to only include rows where category_col is in the list of categories.

    Parameters:
        df: pd.DataFrame
        category_col: str, name of the column containing category codes
        categories: list of str, valid category codes

    Returns:
        Filtered pd.DataFrame
    """
    return df[df[category_col].isin(categories)].copy()


def map_categories_to_products(df, category_col, mapping):
    """
    Map category codes to higher-level product names and store in a new 'Product' column.

    Parameters:
        df: pd.DataFrame
        category_col: str, name of the column containing category codes
        mapping: dict, maps category codes to product strings

    Returns:
        pd.DataFrame with new 'Product' column
    """
    df['Product'] = df[category_col].map(mapping)
    return df


def preprocess_data(
    file_obj,
    category_col='SERVICE_CATEGORY',
    date_cols=['ACCEPTANCE_TIME', 'COMPLETION_TIME'],
    categories=None,
    mapping=None
):
    """
    Full preprocessing pipeline for ticket data:
      1. Load raw data from text file
      2. Parse date columns
      3. Drop rows with invalid acceptance dates
      4. Filter to relevant ticket categories
      5. Map categories to product groups
      6. Drop unmapped rows
      7. Sort by acceptance time

    Parameters:
        file_obj: file-like object or path to data file
        category_col: str, column in raw data representing category
        date_cols: list of str, date/time columns to parse
        categories: list of str, valid category codes to retain
        mapping: dict, mapping from category codes to product names

    Returns:
        pd.DataFrame ready for analysis (with datetime columns and 'Product')
    """
    # Default categories and mapping if not provided
    if categories is None:
        categories = ['NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']
        # with hardware
        # categories = ['HDW', 'NET', 'KAI', 'KAV', 'GIGA', 'VOD', 'KAD']
    if mapping is None:
        mapping = {
            'KAI': 'Broadband',
            'NET': 'Broadband',
            'KAV': 'Voice',
            'KAD': 'TV',
            'GIGA': 'GIGA',
            'VOD': 'VOD'
            # 'HDW': 'Hardware'
        }

    # 1. Load raw data
    df = load_raw_data(file_obj)

    # 2. Parse date columns
    df = parse_dates(df, date_cols)

    # 3. Drop rows with invalid acceptance dates
    df = df.dropna(subset=['ACCEPTANCE_TIME'])

    # 4. Filter by category
    df = filter_by_category(df, category_col, categories)

    # 5. Map categories to products
    df = map_categories_to_products(df, category_col, mapping)

    # 6. Drop rows where mapping failed
    df = df.dropna(subset=['Product'])

    # 7. Sort by acceptance time
    df = df.sort_values('ACCEPTANCE_TIME')

    return df
