from django.core.management.base import BaseCommand
from backend.settings import BASE_DIR, DATABASE_URL
from api.models import weatherData, weatherStats

import os
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

repo_owner = 'corteva'
repo_name = 'code-challenge-template'
data_folder= 'wx_data'
file_path = os.path.join(BASE_DIR, 'tmp')
gitHub_api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/zipball/main'

class Command(BaseCommand):
    help = "This command will add data from the corteva coding project github repository to the database"

    def handle(self, *args, **kwargs):
        ############
        # Download data from GitHub
        ############
        # if its already downloaded...
        if os.path.exists(file_path):
            # Get the name of the downloaded github repo
            # first list the files in the path (should only be one)
            items = os.listdir(file_path)
            # grab the first item (again there is only one)
            local_repo_path = str(next((item for item in items if os.path.isdir(os.path.join(file_path, item))), None))
        # otherwise download it
        else:
            # Create a target directory for storing the github repo
            os.makedirs(file_path, exist_ok=True)
            # Make a GET request to the GitHub API to get the ZIP archive
            response = requests.get(gitHub_api_url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the ZIP content
                with ZipFile(BytesIO(response.content)) as zip_file:
                    # Extract only the contents of the specific folder from the ZIP archive
                    zip_file.extractall(file_path)
                    # Get the name of the downloaded github repo
                    # first list the files in the path (should only be one)
                    items = os.listdir(file_path)
                    # grab the first item (again there is only one)
                    local_repo_path = str(next((item for item in items if os.path.isdir(os.path.join(file_path, item))), None))
            else:
                # Print an error message if the request was not successful
                print(f"Error: Unable to fetch folder {repo_name}. Status code: {response.status_code}")
        ############
        # Ingest the Data into pandas
        ############
        try: 
            # store the name of the directory where data files we want to ingest are located
            source_dir = os.path.join(file_path, local_repo_path, data_folder)
            # Get the list of file names in the data source directory
            files_to_fetch = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
            # column names of tsv weather data files
            cols_source = ['date','max_temp','min_temp','precip']
            # column names of our pandas df
            cols_dest = ['station','date','year','month','day','max_temp','min_temp','precip']
            #create empty dataframe to add iterations of loaded files into
            df = pd.DataFrame(columns=cols_dest)
            # iterate through the data files, load them into pandas, transform them, and then append them to df
            for file in files_to_fetch:
                data = pd.read_csv(f'{source_dir}/{file}', sep='\t', names=cols_source)
                data['station'] = os.path.splitext(file)[0]
                data['year'] = data['date'].astype(str).str[:4].astype(int)
                data['month'] = data['date'].astype(str).str[4:6].astype(int)
                data['day'] = data['date'].astype(str).str[6:].astype(int)
                # convert the -9999 to pandas missing values
                data.replace(-9999, np.nan, inplace=True)
                # append station data file to main df
                df = pd.concat([df, data], axis=0, ignore_index=True)
        except Exception as e:
            print(f"Unable to ingest data into pandas. Error: {e}")
        ############
        # Calculate summary statistics
        ############
        if not df.empty:
            # using groupby, calculate summary statics for each station for each year. skip na values specific to each column
            stats = df.groupby(['station', 'year']).agg({'max_temp': ['mean'], 'min_temp': ['mean'], 'precip': ['sum']}, skipna=True).reset_index()
            # Flatten the multi-level column index created by groupby
            stats.columns = ['_'.join(col).strip() for col in stats.columns.values]
            # Rename columns
            stats = stats.rename(columns={'station_': 'station', 'year_': 'year', 'max_temp_mean': 'max_temp_mean',
                                        'min_temp_mean': 'min_temp_mean', 'precip_sum': 'total_precip'})
            # Specify the number of significant figures for each column
            significant_figures = {'max_temp_mean': 2, 'min_temp_mean': 2, 'total_precip': 0}
             # Round the summary stats to the specified number of significant figures
            for col, sig_figs in significant_figures.items():
                stats[col] = stats[col].round(sig_figs)
        else:
            pass
        ############
        # Load data into database models
        ############
        # setup Database engine 
        engine = create_engine(DATABASE_URL, echo=False)
        # bulk insert pandas dataframes into database, if data already in table replace it. 
        stats.to_sql(weatherStats._meta.db_table, if_exists='replace',  con=engine, index=True)
        df.to_sql(weatherData._meta.db_table, if_exists='replace', con=engine, index=True)
        