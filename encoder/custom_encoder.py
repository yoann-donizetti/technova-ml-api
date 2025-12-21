import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder

class CustomEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, bool_cols=None, cat_onehot_cols=None, num_cols=None):
        self.bool_cols = bool_cols or []
        self.cat_onehot_cols = cat_onehot_cols or []
        self.num_cols = num_cols or []

    def fit(self, X, y=None):
        # Stockage des colonnes
        self.bool_cols_ = list(self.bool_cols)
        self.cat_onehot_cols_ = list(self.cat_onehot_cols)
        self.num_cols_ = list(self.num_cols)

        # OneHot
        self.ohe_ = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        if self.cat_onehot_cols_:
            self.ohe_.fit(X[self.cat_onehot_cols_])

        return self

    def transform(self, X):
        parts = []

        # Booléens
        if self.bool_cols_:
            df_bool = X[self.bool_cols_].astype(int)
            parts.append(df_bool)

        # Numériques
        if self.num_cols_:
            df_num = X[self.num_cols_]
            parts.append(df_num)

        # OneHot
        if self.cat_onehot_cols_:
            ohe_data = self.ohe_.transform(X[self.cat_onehot_cols_])
            ohe_df = pd.DataFrame(
                ohe_data,
                columns=self.ohe_.get_feature_names_out(self.cat_onehot_cols_),
                index=X.index
            )
            parts.append(ohe_df)

        # Fusion
        df_final = pd.concat(parts, axis=1)

        # Stockage des colonnes finales (utile pour FI)
        self.feature_names_ = df_final.columns.tolist()

        return df_final