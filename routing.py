from datetime import timedelta

from distance_loader import get_distance, get_address_index


# Delivers the packages assigned to a truck using a
# nearest-neighbor routing algorithm.
def deliver_packages(truck, package_table, addresses, distances):
    undelivered = truck.packages.copy()

    # Record when each package leaves the hub with this truck.
    for package_id in truck.packages:
        package = package_table.lookup(package_id)
        package.departure_time = truck.departure_time

    while undelivered:
        nearest_package = None
        nearest_distance = float("inf")
        nearest_location = None

        for package_id in undelivered:
            package = package_table.lookup(package_id)
            package_location = get_address_index(addresses, package.address)

            distance = get_distance(
                distances,
                truck.current_location,
                package_location
            )

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package
                nearest_location = package_location

        # Move the truck to the nearest package location.
        truck.mileage += nearest_distance
        truck.current_location = nearest_location

        # Calculate travel time based on the truck's 18 mph speed.
        travel_hours = nearest_distance / truck.speed
        travel_minutes = travel_hours * 60

        truck.current_time += timedelta(minutes=travel_minutes)

        # Mark the package as delivered at the truck's current time.
        nearest_package.status = "Delivered"
        nearest_package.delivery_time = truck.current_time

        # Remove the delivered package from the remaining packages.
        undelivered.remove(nearest_package.package_id)

    # Return the truck to the hub after all packages are delivered.
    distance_to_hub = get_distance(
        distances,
        truck.current_location,
        0
    )

    truck.mileage += distance_to_hub

    travel_hours = distance_to_hub / truck.speed
    travel_minutes = travel_hours * 60

    truck.current_time += timedelta(minutes=travel_minutes)

    # The truck is now back at the hub.
    truck.current_location = 0