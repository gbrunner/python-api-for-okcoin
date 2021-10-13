import os
import datetime
import time
import configparser
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def upload_to_azure_storage(df,
                            config_file="azure.config",
                            connection_string=None,
                            data_path=None,
                            container_name=None,):
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
        >>> acc = Account(r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\auth.config")
        >>> ledger = acc.get_ledger()
        >>> dm.upload_to_azure_storage(ledger.df,  r"C:\Users\gbrunner\Documents\GitHub\python-api-for-okcoin\src\azure.config")
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
    local_file_name = "ledger_" + st + ".csv"
    upload_file_path = os.path.join(data_path, local_file_name)

    # Write text to the file
    #file = open(upload_file_path, 'w')
    #file.write("date, data, account, value")
    #file.close()
    csv = df.to_csv(upload_file_path)

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    print(blob_client.account_name)
    print(blob_client.blob_name)
    print(blob_client.container_name)

    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

    return blob_client.account_name, blob_client.container_name, blob_client.blob_name
