import os
import datetime
import time
import configparser
import pandas as pd
from io import  StringIO
import plotly.graph_objects as go
from azure.storage.blob import BlobServiceClient


def upload_to_azure_storage(df,
                            config_file="azure.config",
                            record_type="ledger",
                            connection_string=None,
                            data_path=None,
                            container_name=None):
    r""" uploads a ledger dataframe as a CSV into a Azure Blob Storage container.
    This is meant to be run daily so that we can track any staking reqards that are deposited daily.

    Parameters
    ----------
    df : DataFrame
        A pandas dataframe of a ledger to be uploaded.

    config_file : str
        The name of the azure config file that holds the connection string, account name, and
        temporary local filesystem location for storing the CSV.

    connection_string : str
        Azure connection string. Must be specified is a config file is not used.

    data_path : str
        Local file path for CSV to be created before uploading to Azure

    container_name : str
        The name of the Azure storage container to uplaod the CSV to.


    Returns
    -------
    blob_client.account_name, blob_client.container_name, blob_client.blob_name : tuple
        returns a tuple of the Azure account name, container name, and CSV file name

    Examples
    --------
    >>> from okcoin import Account
    >>> import okcoin.DataMangement as dm
    >>> acc = Account(r"C:\auth.config")
    >>> ledger = acc.get_ledger()
    >>> dm.upload_to_azure_storage(ledger.df,  r"C:\azure.config")
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    # Create a local directory to hold blob data
    connection_string = config['DEFAULT']['connection_string']  # secret_key
    data_path = config['DEFAULT']['data_path']
    container_name = config['DEFAULT']['container_name']

    # Create a file in the local data directory to upload and download
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    local_file_name = record_type+"_" + st + ".csv"
    upload_file_path = os.path.join(data_path, local_file_name)

    # Write text to the file
    csv = df.to_csv(upload_file_path)

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    print(blob_client.account_name)
    print(blob_client.blob_name)
    print(blob_client.container_name)

    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

    return blob_client.account_name, blob_client.container_name, blob_client.blob_name


def dataframe_from_azure_storage(config_file="azure.config",
                            filter="ledger",
                            connection_string=None,
                            data_path=None,
                            container_name=None):
    r""" Retrieves all of the ledger data stored in Azure blob storage.

    Parameters
    ----------
    config_file : str
        The name of the azure config file that holds the connection string, account name, and
        temporary local filesystem location for storing the CSV.

    connection_string : str
        Azure connection string. Must be specified is a config file is not used.

    data_path : str
        Local file path for CSV to be created before uploading to Azure

    container_name : str
        The name of the Azure storage container to uplaod the CSV to.


    Returns
    -------
    df : DataFrame
        Returns a data frame of all historical ledger information.

    Examples
    --------
    >>> from okcoin import Account
    >>> import okcoin.DataMangement as dm
    >>> df = dm.dataframe_from_azure_storage(r"C:\azure.config")
    >>> print(df)
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    # Create a local directory to hold blob data
    connection_string = config['DEFAULT']['connection_string']  # secret_key
    data_path = config['DEFAULT']['data_path']
    container_name = config['DEFAULT']['container_name']

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service_client.get_container_client(container_name)

    print("\nListing blobs...")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    #for bl in blob_list:
    #    if filter in bl.name:
    #        print(bl.name)

    start = True
    for idx, blob in enumerate(blob_list):
        if filter in blob.name:
            print("\t" + blob.name)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
            data = blob_client.download_blob().readall()

            if start: #idx == 0:
                start = False
                df = pd.read_csv(StringIO(data.decode("utf-8")))
            else:
                t_df = pd.read_csv(StringIO(data.decode("utf-8")))
                df = pd.concat([df, t_df])
                del t_df

    df.reset_index(inplace=True)
    try:
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        print("No column to drop.")
    try:
        df.drop(['index'], axis=1, inplace=True)
    except:
        print("No column to drop.")

    df.drop_duplicates(keep='first', subset=['ledger_id'], inplace=True)

    return df

def plot_staking_history(df, currency='BTC'):
    r""" Creates a Plotly chart of the asset that you want to plot.

    Parameters
    ----------
    df : DataFrame
        A dataframe consisting of the ledger information that you want to plot.

    currency : str
        The currency you want to plot, for example, 'BTC'.


    Returns
    -------
    fig : Figure
        Returns a Plotly graph object figure.

    Examples
    --------
    >>> import okcoin.DataMangement as dm
    >>> df = dm.dataframe_from_azure_storage(r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\azure.config")
    >>> chart = dm.plot_staking_history(df, 'BTC')
    """

    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
    cur = df[df['currency'] == currency]
    cur_balance = cur.groupby('timestamp')['balance'].max()
    balance = cur_balance.to_frame()
    balance.reset_index(inplace=True)

    fig = go.Figure(data=go.Scatter(
        x=balance.timestamp.tolist(),
        y=balance.balance.tolist(),
        mode='markers'
    ))

    fig.update_layout(
        title=currency,
        xaxis_title="Date",
        yaxis_title="Value in " + currency)

    return fig


def upload_ledger_history():
    from okcoin import Account
    acc = Account(r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\auth.config")
    ledger = acc.get_ledger()
    df = upload_to_azure_storage(ledger.df,
                                 r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\azure.config",
                                 "ledger")
    return df


def upload_order_history(pairs=['STX-USD', 'MIA-USD','XTZ-USD'], state=7):
    from okcoin import Spot
    spot = Spot(r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\auth.config")
    for idx,pair in enumerate(pairs):
        orders = spot.get_order_list(pair, state=str(state))
        if idx == 0:
            df = orders.df
        else:
            t_df = orders.df
            df = pd.concat([df, t_df])

    df.reset_index(inplace=True)

    upload_to_azure_storage(df,
                            r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\azure.config",
                            "filled_orders")

    return df