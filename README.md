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
