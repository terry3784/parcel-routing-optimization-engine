import csv

from package import Package

# Loads package data from the WGUPS CSV file and stores each package
# in the custom hash table using the package ID as the key.
def load_package_data(filename, package_table):
    with open(filename, mode="r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)

        # Skip header and blank rows that do not contain a package ID.
        for row in csv_reader:
            if not row or not row[0].strip().isdigit():
                continue

            # Extract package information from the current CSV row.
            package_id = int(row[0])
            address = row[1].strip()
            city = row[2].strip()
            state = row[3].strip()
            zip_code = row[4].strip()
            deadline = row[5].strip()
            weight = row[6].strip()
            notes = row[7].strip()

            # Create a Package object using the information from the CSV.
            package = Package(
                package_id,
                address,
                city,
                state,
                zip_code,
                deadline,
                weight,
                notes
            )

            # Store the package in the hash table using its ID as the key.
            package_table.insert(package_id, package)