#!/usr/bin/env python3

import csv
from shapely.geometry import Point
import geopandas as gp

# Any column not listed will not be included in the output csv
columns = [
	"latitude",
	"longitude",
	"room_type",
	"price",
	"minimum_nights",
	"number_of_reviews",
]

# Define boundary of seattle
seattle = gp.read_file("seattle.geojson")
seattle = seattle.to_crs("EPSG:4326")
seattle_boundary = seattle.geometry.union_all()

seen_rows = []

# Find rows differing by 0 or 1 column
def find_unique_rows(rows):
	conflicts = set()

	for i, a in enumerate(rows):
		for b in rows[i + 1:]:
			diff = [c for c in columns if a[c] != b[c]]

			if len(diff) <= 1:
				conflicts.add(tuple(a[c] for c in columns))
				conflicts.add(tuple(b[c] for c in columns))
				print(f"Conflict at Coordinates: {a['latitude']}, {a['longitude']}")
				print(f"	Differing columns: {[(c, a[c], b[c]) for c in diff]}")
				print()

	return [r for r in rows if tuple(r[c] for c in columns) not in conflicts]

# Clean the data, write to listings_dirty.csv
with open("data/listings.csv", "r", newline="", encoding="utf-8") as infile:
	reader = csv.DictReader(infile)
	seen = set()

	with open("listings_dirty.csv", "w", newline="", encoding="utf-8") as outfile:
		writer = csv.DictWriter(outfile, fieldnames=columns)
		writer.writeheader()
		filtered_rows = [
			row for row in reader

			# Keep any rows that have NO empty values
			if all(row[col] and row[col].strip() for col in columns)

			# Keep any coordinates greater than 0.001 precision - This precision "Same Street"
			and len(row["latitude"].split(".")[-1]) >= 3
			and len(row["longitude"].split(".")[-1]) >= 3

			# Remove any coordinates not in Seattle
			# (Nothing removed using this filter, leaving it in for now though)
			and seattle_boundary.covers(
				Point(float(row["longitude"]), float(row["latitude"]))
			)
		]

		# Sort and keep all unique rows
		unique_rows = find_unique_rows(filtered_rows)

		# Write to the file
		writer.writerows(
			{col: row[col] for col in columns}
			for row in unique_rows
		)
