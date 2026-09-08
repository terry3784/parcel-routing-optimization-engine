import csv

# Loads the distance CSV and separates the location information
# from the distance matrix used by the routing algorithm.
def load_distance_data(filename):
    with open(filename, mode="r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    # Skip the first eight rows, which contain header and descriptive
    # information rather than actual WGUPS location data.
    distance_rows = rows[8:]

    addresses = []
    distances = []

    # Store each location and its corresponding row of distance values.
    # Distance values begin at column index 2 in the CSV.
    for row in distance_rows:
        addresses.append(row[0])
        distances.append(row[2:])

    return addresses, distances


# Returns the distance between two locations in the distance matrix.
# The distance table contains only one half of the symmetric matrix,
# so if one direction is blank, the reverse direction is checked.
def get_distance(distances, location_1, location_2):
    distance = distances[location_1][location_2]

    if distance == "":
        distance = distances[location_2][location_1]

    # CSV values are strings, so convert the mileage to a float
    # before returning it for routing and mileage calculations.
    return float(distance)


# Finds the location index in the distance table that matches
# a package's street address.
def get_address_index(addresses, package_address):
    normalized_package_address = package_address.lower().replace("station", "sta")

    for index, address in enumerate(addresses):
        normalized_distance_address = address.lower()

        if normalized_package_address in normalized_distance_address:
            return index

    return None



