
def sanitize(df):
    # sanitize the dataset to be safe for ML models
    # drop columns with missing values
    colmissing = [col for col in df.columns
                     if df[col].isnull().any()]
    df = df.drop(colmissing ,axis = 1)
    # drop categorical variables
    df = df.select_dtypes(exclude=['object'])
    return df