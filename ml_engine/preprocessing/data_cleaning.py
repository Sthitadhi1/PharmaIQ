import pandas as pd


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    return df.fillna(method='ffill').fillna(method='bfill')


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def normalize_features(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    normalized = df.copy()
    for column in columns:
        if column in normalized.columns and pd.api.types.is_numeric_dtype(normalized[column]):
            min_val = normalized[column].min()
            max_val = normalized[column].max()
            if max_val != min_val:
                normalized[column] = (normalized[column] - min_val) / (max_val - min_val)
    return normalized
