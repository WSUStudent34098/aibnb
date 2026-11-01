# aibnb - A school project
## Cleaning
### Keep only relevant columns:
| Preserved Columns |
| :---: |
| latitude |
| longitude |
| room_type |
| price |
| minimum_nights |
| number_of_reviews |
### Keep any rows that have NO empty values
This means any row with an empty value in any of the above columns will be removed.
### Keep any coordinates greater than 0.001 precision
This precision is "Same Street" accuracy, excluding values that are not even close to the true address.
### Remove any coordinates not in Seattle
We are looking only within Seattle boundaries. The included "geojson" is an official Seattle document.
### Sort and keep all unique rows
Once all rows are sorted, they are checked for uniqueness. Any duplicate rows are deleted, as well as any rows differing by only one column.
If a row differs by one column, all rows detected are deleted. The loss is minimal, and it logs to STDOUT which rows are removed.
### Ingestion
Once the CSV file is processed, the data can be directly ingested into a database. This has been tested, showing zero errors so far.

## Training  
### Load cleaned data from cleaning step
Currently only 1 model is trained for this milestone. The training process loads from a pre-cleaned file to avoid duplicating work shared between models.  
### Separate target from predictors  
The model targets priced based on the rest of the data present in the preserved columns.  
### Partition training and test data  
80% of the test set is for training and 20% is for testing and are partitioned on room type. This split was chosen such that the rarest room types are guaranteed to have at least 2 elements in the test set, as the rarest room type (shared room) has only 10 entries in the clean dataset. 
### Enumerate room type  
Full house/apartment is treated as the default room type. The remaining room types are trained as 0/1 indicators on if it is true, and the coefficients on them are the adjustments for their room type.  
### Train and score  
The model is trained and scored on several metrics, printed to the console. For the next milestone, adjustments will be made to the training approach to determine the best model that can be trained from this dataset based on these metrics.  
### Save the model to a file
The model is then saved to a file for the harness to utilize, to avoid retraining the model for each interactive prediction made by the user. 