import os
import zipfile
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# Function to collect historical gold price data
def collect_data(kaggle_username, kaggle_api_key):
    try:
        # Authenticate with Kaggle
        api = KaggleApi()
        api.authenticate(username=kaggle_username, key=kaggle_api_key)

        # Search for the dataset containing historical gold price data
        datasets = api.dataset_list(search='gold price')

        # Verify and select the desired dataset
        for dataset in datasets:
            if 'gold' in dataset.title.lower() and 'price' in dataset.title.lower():
                dataset_id = dataset.ref
                break
        else:
            print("Error: Dataset containing historical gold price data not found.")
            return None

        # Download dataset files
        api.dataset_download_files(dataset_id, path='./gold_price_data', unzip=True)

        # Find the CSV file
        csv_file = [file for file in os.listdir('./gold_price_data') if file.endswith('.csv')]
        if not csv_file:
            print("Error: CSV file containing historical gold price data not found.")
            return None
        csv_file_path = os.path.join('./gold_price_data', csv_file[0])

        # Read the CSV file
        data = pd.read_csv(csv_file_path)

        # Cleanup: Delete downloaded files
        os.remove(csv_file_path)
        os.rmdir('./gold_price_data')

        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None