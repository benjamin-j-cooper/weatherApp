from django.core.management.base import BaseCommand
from backend.settings import BASE_DIR, DATABASE_URL
from api.models import weatherData, weatherStats

import os
import time 
from datetime import datetime
import requests
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import logging

import warnings # prevent python warnings from printing to the console                                
warnings.filterwarnings('ignore')

logger = logging.getLogger('django')


class Command(BaseCommand):
    help = "This command will add data from the corteva coding project github repository to the database"

    def handle(self, *args, **kwargs):
        repo_owner = 'corteva'
        repo_name = 'code-challenge-template'
        data_folder= 'wx_data'
        file_path = os.path.join(BASE_DIR, 'tmp')
        gitHub_api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/zipball/main'
        
        ############
        # Download data from GitHub
        ############
        start_time = time.time()
        print('='*40)
        print('Downloading github repo...')
        print('='*40)
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
            print('='*40) 
            print('Performing data processing...')
            print('='*40)
            # store the name of the directory where data files we want to ingest are located
            source_dir = os.path.join(file_path, local_repo_path, data_folder)
            # Get the list of file names in the data source directory
            files_to_fetch = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
            # column names of tsv weather data files
            cols_source = ['date','max_temp','min_temp','precip']
            # column names of our pandas df
            cols_dest = ['station','date','year','max_temp','min_temp','precip']
            #create empty dataframe to add iterations of loaded files into
            df = pd.DataFrame(columns=cols_dest)
            # iterate through the data files, load them into pandas, transform them, and then append them to df
            for file in files_to_fetch:
                data = pd.read_csv(f'{source_dir}/{file}', sep='\t', names=cols_source)
                data['station'] = os.path.splitext(file)[0]
                #convert the -9999 to pandas missing values
                data.replace(-9999, np.nan, inplace=True)
                #split apart data into single fields
                data['year'] = data['date'].astype(str).str[:4].astype(int)
                # data['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d', errors='coerce')
                # data['date'] = df['date'].dt.strftime('%Y-%m-%d')
                #convert temps from tenth of a degree C to degrees celcius
                data['max_temp'] = data['max_temp'] / 10 
                data['min_temp'] = data['min_temp'] / 10
                #convert precip from tenth of a mm to centimeters
                data['precip'] = data['precip'] / 100
                # append station data file to main df
                df = pd.concat([df, data], axis=0, ignore_index=True)
        except Exception as e:
            print(f"Unable to ingest data into pandas. Error: {e}")
        ############
        # Calculate summary statistics
        ############
        if not df.empty:
            print('='*40)
            print('Calculating summary stats...')
            print('='*40)
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
        # Running QA/QC checks on data
        ############ 
        print('='*40)
        print('Running QA/QC checks on data...')
        print('='*40)

        # check temps
        min_temp = -273.15  # Define minimum allowable temperature for celcius
        max_temp = 56.7  # Define maximum allowable temperature for celcius
        # Check if temps are in celcius range
        max_temps_are_between_range = (df['max_temp'] >= min_temp) & (df['max_temp'] <= max_temp)
        min_temps_are_between_range = (df['min_temp'] >= min_temp) & (df['min_temp'] <= max_temp)

        max_values_between_range = max_temps_are_between_range.all()
        min_values_between_range = min_temps_are_between_range.all()

        if not max_values_between_range and min_values_between_range:
            print('QA/QC WARNING: temperature values outside of logical Celcius range!')

        # check dates
        start_date = 19850101
        end_date = 20141231
        # Check if dates are between start_date and end_date
        is_between_dates = (df['date'] >= start_date) & (df['date'] <= end_date)
        all_dates_between_range = is_between_dates.all()

        if not all_dates_between_range:
            print('QA/QC WARNING: dates are outside of specified date range!')
            
        
        ############
        # Load data into database models
        ############
    
        print('='*40)
        print('Inserting data into Postgres...')
        print('='*40)

        # Establish a connection to the PostgreSQL database
        engine = create_engine(DATABASE_URL, echo=False)

        #print to logger
        logger.info(f'Django command appData called: {datetime.now()}')
        logger.info(f'Start time of data ingestion: {start_time}')
        logger.info(f'Dataframe Null values: \n{df.isnull().sum()}')

        # weather data
        records_count, new_records = self.insert_data_pgdb(df, weatherData, engine)
        # logging
        logger.info(f'{new_records} records added to weatherdata table')
        logger.info(f'{records_count} records in weatherdata table')

        # stats
        records_count, new_records = self.insert_data_pgdb(stats, weatherStats, engine)
        # logger
        logger.info(f'{new_records} records added to stats table')
        logger.info(f'{records_count} records in weatherdata table')

        #make end time, get elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        # logger
        logger.info(f'End time of data ingestion: {end_time}')
        logger.info(f'Data ingestion completed in: {elapsed_time} seconds')


        print('='*40)
        print(f'Completed Data ingestion in {elapsed_time} seconds')
        print('='*40)


    def insert_data_pgdb(self, dataframe, dataModel, engine):
        pgdb_table = dataModel._meta.db_table
        try:
            # Check if the database table is empty
            if dataModel.objects.count() == 0:
                #database table is empty. To speed up the ingestion, bulk insert all records.
                dataframe.to_sql(pgdb_table, if_exists='replace', con=engine, index=True,index_label='id')
                new_records = dataframe.shape[0]
                records_count = dataModel.objects.count()

                return records_count, new_records
            
            else:
                # Check if records already exist in the database
                existing_records = pd.read_sql_query(f'SELECT * FROM {pgdb_table}', engine)
                existing_keys = set(existing_records.apply(lambda row: self.generate_key(row, pgdb_table), axis=1))
                new_records = dataframe[~dataframe.apply(lambda row: self.generate_key(row, pgdb_table), axis=1).isin(existing_keys)]

                if not new_records.empty:
                    new_records.to_sql(pgdb_table, if_exists='append', con=engine, index=True, index_label='id')
                    new_records = len(new_records)
                    records_count = dataModel.objects.count()
                else:
                    new_records = 0
                    records_count = dataModel.objects.count()
                    
                return records_count, new_records
        except Exception as e:
            print(f"Error adding records to the database: {e}")
            logger.info(f"Error adding records to the database: {e}")

    def generate_key(self, row, pgdb_table):
        if pgdb_table in 'api_weatherdata':
            # Combine 'station' and 'date' fields to create a composite key
            return f"{row['station']}_{row['date']}"
        else:
            return f"{row['station']}_{row['year']}"