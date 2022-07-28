# Practical tasks using Cognite Python SDK
In this section learner need to perform various tasks such as
- Example dataset uploading and creation of various resource types
- Retrieve, explore and update the data
- Cleanup

## Use-case and Data overview
The data used in this section is downloaded from internet. It's the data about various countries.
- First an asset hierarchy need to be created for mapping between Geographical regions and countries.
- Then step by step various data from sources like World Bank, United Nations etc is added at a country level.

## 0. Create the Cognite Client
The first step is to connect to Cognite Data Fusion. Use the Authentication script file from utils and create a cognite client.

## 1. Create a dataset
- Create a dataset with name such as "world_info" or "global_info". 
- Make sure it is write protected.
- Get the dataset id of the dataset and save as `ds_id`

## 2. Create the Asset Hierarchy
- Obtain the United Nations Location Codes data from this URL https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv
- Read the csv file in a datarame in notebook (e.g. world_df ).
- Create a Root Asset called "world" with proper description and associate it with the dataset using ds_id.
- After creating the root asset, update the Name of the Asset.( Change it to "Global" or "my_world" )
- Get the list of the the regions from the world_df and create Region level assets under Root asset.
- Next, Get the list of Country & Region pairs from the world_df and create the country level assets under each region asset.
- Finally, Use the code or Go to CDF UI, To verify if the asset hierarchy is created as defined in above steps.

Note : If the required assets are already created in the tenant, then it's better to add a unique prefix or suffix to the external_ids & names to distinguish and avoid the duplicated errors.

## 3. Add Data for each country

### 3.1 Add timeseries
- Get the World Population Data over the years https://data.worldbank.org/indicator/SP.POP.TOTL
using worldbank API (wbgapi) package. ( You can decide the duration e.g. take last 20 years i.e. 2000-2020)
- Create the population timeseries for each country asset and Insert the data from world bank in those timeseries.

### 3.2 Add some files
- PDF Files data for each country by UN https://unctadstat.unctad.org/CountryProfile/GeneralProfile/en-GB/012/index.html
- Get the PDF files by passing the Country Code( 3 digit code ) to this URL
https://unctadstat.unctad.org/CountryProfile/GeneralProfile/en-GB/{CountryCode}/GeneralProfile{CountryCode}.pdf
- Upload the files for each country under it's own asset. Also specify the dataset ID. ( Upload 10-20 files, no need to upload for all the countries)

Downloading files with code might require a bit of web scrapping code, but you can also do manually for some countries.

### 3.3 Add events
- Events data e.g. All disasters by Country https://public.emdat.be/data
- Create an account and download the latest data from the above URL.
- Download all types of events in the whole world.
- Read the downloaded excel file in notebook.
- Create the events from this data, for each country. 

Note : A historical file of these events is available in data folder.

### 3.4 Add Labels
- Create labels such as "Cold" or "Hot" climate countries.
- Apply these labels to some countries. (e.g. Cold to "Canada", "Norway"  & Hot to "Ghana","Qatar")

## 4. Retrieve Data
Retrieve the population time series data for some countries and plot it.

## 5. Final Task:  Delete the data ( Cleanup )
In this step, you need to delete everything which you've added in the previous steps or tasks.
- First delete the root asset, then delete all the subtree asssets.
- Verify, that for the given dataset ("world_info"), there are no assets left or exists.
- Delete all the timeseries, labels, events, sequences etc created for each asset.


