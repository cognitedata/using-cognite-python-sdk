# Practical tasks using Cognite Python SDK

In this hands-on exercise, you will perform the following tasks:
- Creating data sets and various CDF resource types
- Retrieving, exploring, and updating data in CDF
- Cleaning up

## Use-case and Data overview

The data used in this exercise will be around mapping geographical regions and countries to assets in CDF. Additionally, we will integrate this asset hierarchy with other sources such as the World Bank and the United Nations.

## Pro-tips before you get started

* Pressing `Tab` in your jupyter-notebook enables code auto-completion.
* Pressing `Shift+Tab` when your cursor is inside a Python function opens up a small pop-up box in the jupyter-notebook. This pop-up shows you the docstring of the function and tells you what the expected function arguments are along with examples of how to use the function.
* When creating resource types in CDF, you typically specify either the `name`, the `external_id`, or both. The external_id in this case is a **human readable unique identifier** that helps you identify your resource type while `name` on the other hand is not unique. Essentially this means that 2 resource types can share the same `name` but cannot have the same `external_id`.
* In this hands-on exercise, we only require you to specify the `name` and not the `external_id`. Feel free to use the `external_id` as well if you want to but bear in mind that you might encounter duplication errors if that `external_id` for that particular resource type has already been created.
* If you encounter duplication errors then it's better to add a unique prefix or suffix to the `external_id` of your resource type. Something like `jack_reacher_<my_external_id>`.


## 0. Create the Cognite Client
The first step is to connect to Cognite Data Fusion. Use the Authentication script file `utils/auth.py` in this repo to instantiate a Cognite client. Note that to use the interactive login you need to be signed up to Cognite Hub (https://auth.hub.cognite.com/).

## 1. Create a Data Set
- Create a data set with the name **"<your_name>_world_info"**.
- Make sure that the data set is write-protected.
- Find the data set id of your newly created data set

## 2. Create the Asset Hierarchy

For the Asset Hierarchy, we will be using the United Nations Location Codes data stored in `data/all_countries.csv`. This can also be obtained from this URL: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv. To create the asset hierarchy, follow the steps below:

- Create an asset called "world" with an appropriate description and associate it with the dataset that you created in the previous section. This will be our **root asset** (i.e. the top-level asset).
- After creating the root asset, update the name of the asset to "global".
- Read the `all_countries.csv` file as a dataframe and list all the unique regions in the world.
- For each geographical region, create a corresponding CDF asset that is under the "global" root asset and is associated with the "world_info" data set.
- Next, create country-level assets using the data from the CSV and link them to their corresponding region-level assets.
-  Finally, check if the asset hierarchy has been correctly created. You can do checks such as double-checking that all country-level assets that are children of the "Europe" region-level assets are correct.

## 3. Adding Time Series Data

For this exercise, we will be using population data from the World Bank (https://data.worldbank.org/indicator/SP.POP.TOTL) to generate time series data for our country assets. A post-processed form of this data can be found in `../data/populations_postprocessed.csv` which can be used for this exercise. To create time series data, follow the steps below:

- Create a time series object for each country asset in CDF called `<country>_population` and associate it with its corresponding country asset. Remember to associate the data as well to the data set that you created. As an example, the time series for Aruba would be called `Aruba_population`.
- Load the data from `populations_postprocessed.csv` into a pandas dataframe.
- Insert the data for each country in this dataframe using `client.time_series.data.insert_dataframe`.
- As a check, retrieve the latest population data for the countries of Latvia, Guatemala, and Benin.
- Calculate the total population of the Europe region using the Asset Hierarchy and the time series data.


## 4. Uploading Files

PDF files for a select number of countries can be found in the repo at `data/files`. This information was provided by the UN and can also be found here: https://unctadstat.unctad.org/CountryProfile/GeneralProfile/en-GB/012/index.html. To ingest the files, do the following:

- Look at the PDFs in `data/files` and determine which asset each file should belong to.
- Upload the files to CDF with the name `<country>_data_sheet` and make sure that they are assigned to the correct asset and the correct data set.
- As a check, list all the files associated with the country of Vanuatu using `client.files.list`

## 5. Adding events

In this part of the exercise, we will be adding event data for some countries. We will be using data from the disasters database which can be accessed here: https://public.emdat.be/data. For simplicity, events data is also available in the repo at `data/events.csv` which covers all natural geological disasters in Europe from 2010. To add these to CDF:

- Load the file `events.csv` into a Pandas DataFrame
- For each row in the dataframe retrieve the following information
    - Start date (which is a combination of the start day, start month, and start year)
    - End date (which is a combination of the end day, end month end year)
    - Disaster Type
    - Disaster Subtype
    - Location
- Map this data to a CDF Event object with the following mapping:
    - start time is simply the **start date** but in milliseconds since Epoch
    - end is the **end date** but in milliseconds since Epoch
    - type is the **Disaster Type**
    - subtype is the **Disaster Subtype**
    - metadata is a dictionary with the location stored as `{'Location':location}`
- Make sure to also specify its corresponding asset id (related to the country the disaster occurred in) and your data set id
- Create the events in CDF
- Using the Python SDK, retrieve all the events that involved Volcanic Activity


## 6. Add Labels

Labels can be used to help easily query relevant data according to pre-defined categories. In the CDF project, we already have 2 labels that represent "Hot" and "Cold" climate countries.

- Find the external ids of these 2 labels in the CDF project
- Apply these labels to some of the country assets (e.g. Cold to "Canada", "Norway"  & Hot to "Ghana", "Qatar")
- Use the Python SDK to query for all countries that have a cold climate
- Bonus: Create your own label and apply it to your own CDF resource types.


## 7. Final Task:  Clean-Up and Delete the Data in your Data Set
In this step, you need to delete everything which you've added in the previous steps or tasks.

- Delete all the **assets** in your data set.
- Delete all the **time series** in your data set.
- Delete all the **files** in your data set.
- Delete all the **events** in your data set.
- Delete any custom **labels** that you may have created (NOTE: please don't remove the cold and hot climate country labels)
