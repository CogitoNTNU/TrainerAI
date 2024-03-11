import pandas as pd

def load(path: str = 'data.csv'):
    # load csv file 'data.csv' into pandas dataframe
    df = pd.read_csv(path, parse_dates=['date'])
    #print(df.describe())

    # Remove hours, minutes, and seconds from the date column
    df['date'] = df['date'].dt.date
    df['date'] = pd.to_datetime(df['date'])
    dates = df.loc[:, 'date']
    # create new dataframe with a row for all dates in the range
    new_df = pd.DataFrame({'date': pd.date_range(start=dates.min(), end=dates.max(), freq='D')})
    # merge the new dataframe with the original dataframe, so that all dates are included
    df = pd.merge(new_df, df, on='date', how='left')
    df.fillna(0, inplace=True)
    return df