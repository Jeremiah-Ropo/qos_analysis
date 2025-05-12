import re
import pandas as pd


# Function to dynamically convert columns to match the trained model.
def convert_columns(df):
    # Your mapping of old column names (with potential variations) to new column names
    new_column_names = {
        'Download': 'Download',
        'Upload': 'Upload',
        'Latency': 'Latency',
        'DNS Lookup': 'DNS Lookup',
        'RSS': 'RSS',
        'Device Model': 'Device Model',
        'Device Brand Name': 'Device Brand Name',
        'Manufacture': 'Manufacture',
        'OS Version': 'OS Version',
        'OS Core': 'OS Core',
        'Battery Charge Level': 'Battery Charge Level',
        'Operator Name': 'Operator Name',
        'Network Type': 'Network Type',
        'Longitude': 'Longitude',
        'Latitude': 'Latitude',
        'State': 'State',
        'Country': 'Country'
    }
    dynamic_mapping = {}
    
    for col in df.columns:
        for key in new_column_names.keys():
            if re.search(key, col, re.IGNORECASE):
                dynamic_mapping[col] = new_column_names[key]

    df = df.rename(columns=dynamic_mapping)
    return df

def convert_to_datetime(df):
    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    return df

def bucket_time_of_day(time):
    if 0 <= time.hour < 12:
        return 'Morning'
    elif 12 <= time.hour < 17:
        return 'Afternoon'
    else:
        return 'Evening'
    
## Function that convert the df['datetime'] to be apply into bucket_time_of_day
def bucket_time_of_day_df(df):
    df['time_of_day'] = df['datetime'].apply(lambda x: bucket_time_of_day(x))
    return df

def device_model_freq(df):
    device_model_freq = df['Device Model'].value_counts(normalize=True)
    df['Device Model'] = df['Device Model'].map(device_model_freq)
    return df
def device_brand_name_freq(df):
    device_brand_name_freq = df['Device Brand Name'].value_counts(normalize=True)
    df['Device Brand Name'] = df['Device Brand Name'].map(device_brand_name_freq)
    return df

def manufacture_freq(df):
    manufacture_freq = df['Manufacture'].value_counts(normalize=True)
    df['Manufacture'] = df['Manufacture'].map(manufacture_freq)
    return df

def os_version_map(df):
    # Create a new column initialized with NaN values
    df['OS Version'] = None

    # Map versions dynamically using string matching
    df.loc[df['OS Version'].str.contains('Android 8.1', case=False, na=False), 'OS Version'] = 3
    df.loc[df['OS Version'].str.contains('Android 11', case=False, na=False), 'OS Version'] = 6
    df.loc[df['OS Version'].str.contains('Android 9', case=False, na=False), 'OS Version'] = 4
    df.loc[df['OS Version'].str.contains('Android 13', case=False, na=False), 'OS Version'] = 8
    df.loc[df['OS Version'].str.contains('Android 12', case=False, na=False), 'OS Version'] = 7
    df.loc[df['OS Version'].str.contains('Android 10', case=False, na=False), 'OS Version'] = 5
    df.loc[df['OS Version'].str.contains('Android 14', case=False, na=False), 'OS Version'] = 9
    df.loc[df['OS Version'].str.contains('Android 8.0', case=False, na=False), 'OS Version'] = 2
    df.loc[df['OS Version'].str.contains('Android 7', case=False, na=False), 'OS Version'] = 1

    return df


def os_core_freq(df):
    os_core_freq = pd.get_dummies(df['OS Core'], prefix='OS Core', dtype=int)
    df = pd.concat([df, os_core_freq], axis=1)
    df.drop('OS Core', axis=1, inplace=True)
    return df

def operation_encoding(df):
    df['Operator Name'] = df['Operator Name'].astype('str').str.strip().replace('<NA>', 'MTN')
    df['Operator Name'] = df['Operator Name'].astype('str').str.replace('9mobile', '9MOBILE')
    df['Operator Name'] = df['Operator Name'].astype('str').str.replace('GlO', 'GLO')
    df = pd.get_dummies(df, columns=['Operator Name'], prefix='Operator_Name', dtype=int)
    return df

def network_type_map(df):
    df['Network Type'] = df['Network Type'].map({'4G LTE': 2, '3G': 1})
    return df

def state_encoding(df):
    df = pd.get_dummies(df, columns=['State'], prefix='State', dtype=int)
    return df

def time_of_day_encoding(df):
    df = pd.get_dummies(df, columns=['time_of_day'], prefix='time_of_day', dtype=int)
    return df

def drop_columns(df):
    df.drop([
        'Device Id', 'Date', 'Time', 'datetime', 'Country'
    ], axis=1, inplace=True)
    return df

# Function to fill in values from the testing DataFrame
def process_testing_dataset(test_df):

    # List of columns (including missing ones in the test data)
    columns = ['Download (Mbps)', 'Upload (Mbps)', 'Latency (ms)', 'DNS Lookup (ms)',
       'RSS (dBm)', 'Device Model', 'Device Brand Name', 'Manufacture',
       'OS Version', 'Battery Charge Level (%)', 'Network Type', 'Longitude',
       'Latitude', 'OS Core_armeabi-v7a', 'Operator_Name_9MOBILE',
       'Operator_Name_AIRTEL', 'Operator_Name_GLO', 'Operator_Name_MTN',
       'City_Delta State', 'City_Ekiti State',
       'City_Federal Capital Territory', 'City_Kogi State', 'City_Lagos State',
       'City_Ogun State', 'City_Ondo State', 'City_Osun State',
       'City_Oyo State', 'time_of_day_Afternoon', 'time_of_day_Evening',
       'time_of_day_Morning']

    # Create a copy of the template for the same number of rows as test_df
    df_filled = pd.DataFrame(0, index=test_df.index, columns=columns)

    # Update the template DataFrame with values from test_df
    df_filled.update(test_df)

    return df_filled

def save_predicted_values(df, prediction):
    df['Cluster'] = prediction
    print(df.head())
    return df

## Function for to convert a dataframe to undergo feature engineering;
def feature_engineering(df):
    df = convert_columns(df)
    df = convert_to_datetime(df)
    df = bucket_time_of_day_df(df)
    df = device_model_freq(df)
    df = device_brand_name_freq(df)
    df = manufacture_freq(df)
    df = os_version_map(df)
    df = os_core_freq(df)
    df = operation_encoding(df)
    df = network_type_map(df)
    df = state_encoding(df)
    df = time_of_day_encoding(df)
    df = drop_columns(df)
    print(df)
    return df

