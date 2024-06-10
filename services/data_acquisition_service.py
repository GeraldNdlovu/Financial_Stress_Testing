import os
import requests
from kaggle.api.kaggle_api_extended import KaggleApi

# Function to collect historical gold price data
def collect_data():
    try:
        # Authenticate with Kaggle (replace 'username' and 'key' with your Kaggle username and API key)
        api = KaggleApi()
        api.authenticate(username='your_kaggle_username', key='your_kaggle_api_key')

        # Search for the dataset containing historical gold price data
        dataset = api.dataset_list(search='gold price')

        # Assuming the first dataset found is the one we want, download it
        dataset_id = dataset[0].ref
        api.dataset_download_files(dataset_id)

        # Extract the downloaded files
        os.system('unzip *.zip')

        # Read the CSV file containing the data
        data = pd.read_csv('filename.csv')  # Replace 'filename.csv' with the actual filename

        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

