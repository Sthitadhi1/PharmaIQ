import pandas as pd


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df.copy()
    return features


def encode_categories(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    encoded = df.copy()
    for column in columns:
        if column in encoded.columns:
            encoded[column] = encoded[column].astype('category').cat.codes
    return encoded


def scale_features(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    scaled = df.copy()
    for column in columns:
        if column in scaled.columns and pd.api.types.is_numeric_dtype(scaled[column]):
            mean = scaled[column].mean()
            std = scaled[column].std()
            if std != 0:
                scaled[column] = (scaled[column] - mean) / std
    return scaled
