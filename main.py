
from datetime import timedelta

from hash_table import HashTable
from data_loader import load_package_data
from distance_loader import load_distance_data
from truck import Truck
from routing import deliver_packages
from package_loader import load_packages


def get_query_time():
    # Ask the user for a time and convert it to a timedelta.
    while True:
        user_time = input("Enter a time in HH:MM format (example 09:30): ")

        try:
            hours, minutes = map(int, user_time.split(":"))

            if 0 <= hours <= 23 and 0 <= minutes <= 59:
                return timedelta(hours=hours, minutes=minutes)

            print("Please enter a valid time.")

        except ValueError:
            print("Invalid format. Please use HH:MM.")


def get_status_display(package, query_time):
    # Return the package status along with the relevant status time.
    status = package.get_status_at_time(query_time)

    if status == "Delayed":
        return "Delayed until 9:05:00"

    if status == "At Hub":
        return "At Hub until " + str(package.departure_time)

    if status == "En Route":
        return "En Route since " + str(package.departure_time)

    if status == "Delivered":
        return "Delivered at " + str(package.delivery_time)

    return status


def display_all_packages(package_table, trucks, query_time):
    # Display package information and status for each truck
    # at the time entered by the user.
    print("\nPackage status at", query_time)

    for truck in trucks:
        print("\n" + "=" * 40)
        print("TRUCK", truck.truck_id)
        print("=" * 40)

        for package_id in sorted(truck.packages):
            package = package_table.lookup(package_id)

            status_display = get_status_display(
                package,
                query_time
            )

            address, city, state, zip_code = package.get_address_at_time(
                query_time
            )

            print(
                "ID:", package.package_id,
                "| Address:", address,
                "| City:", city,
                "| State:", state,
                "| ZIP:", zip_code,
                "| Deadline:", package.deadline,
                "| Weight:", package.weight,
                "| Status:", status_display
            )


def display_single_package(package_table, package_id, query_time):
    # Display the information and status of one package
    # at the time entered by the user.
    package = package_table.lookup(package_id)

    if package is None:
        print("Package not found.")
        return

    status_display = get_status_display(
        package,
        query_time
    )

    address, city, state, zip_code = package.get_address_at_time(
        query_time
    )

    print("\nPackage status at", query_time)
    print("-" * 100)

    print(
        "ID:", package.package_id,
        "| Address:", address,
        "| City:", city,
        "| State:", state,
        "| ZIP:", zip_code,
        "| Deadline:", package.deadline,
        "| Weight:", package.weight,
        "| Status:", status_display
    )


def main():
    print("Logistics Routing & Dispatch Engine")

    # Create the package hash table and load the package data.
    package_table = HashTable()
    load_package_data("packages.csv", package_table)

    # Load the locations and distance matrix.
    addresses, distances = load_distance_data("distances.csv")

    # Create the three delivery trucks with their initial departure times.
    truck_1 = Truck(1, timedelta(hours=8))
    truck_2 = Truck(2, timedelta(hours=9, minutes=5))
    truck_3 = Truck(3, timedelta(hours=10, minutes=20))

    # Store the trucks in a list so package assignments can be
    # handled by the package-loading algorithm.
    trucks = [truck_1, truck_2, truck_3]

    # Assign packages according to delivery constraints and
    # available truck capacity.
    load_packages(trucks, package_table)

    # Update Package 9 with the corrected address available at 10:20 AM.
    package_9 = package_table.lookup(9)
    package_9.address = "410 S State St"
    package_9.city = "Salt Lake City"
    package_9.state = "UT"
    package_9.zip_code = "84111"

    # Run the first two truck routes using the nearest-neighbor algorithm.
    deliver_packages(truck_1, package_table, addresses, distances)
    deliver_packages(truck_2, package_table, addresses, distances)

    # Only two drivers are available. Truck 3 must wait until a driver
    # returns to the hub and Package 9's corrected address is available.
    driver_available_time = min(
        truck_1.current_time,
        truck_2.current_time
    )

    package_9_available_time = timedelta(hours=10, minutes=20)

    truck_3.departure_time = max(
        driver_available_time,
        package_9_available_time
    )

    truck_3.current_time = truck_3.departure_time

    # A returning driver can now operate Truck 3.
    deliver_packages(
        truck_3,
        package_table,
        addresses,
        distances
    )

    # Calculate and display the combined mileage of all trucks.
    total_mileage = (
        truck_1.mileage
        + truck_2.mileage
        + truck_3.mileage
    )

    print(
        "\nTotal mileage:",
        round(total_mileage, 1),
        "miles"
    )

    # Allow the user to look up package information at any requested time.
    while True:
        print("\nPackage Status Lookup")
        print("1. View all package statuses at a specific time")
        print("2. View one package at a specific time")
        print("3. Exit")

        choice = input("Enter selection: ")

        if choice == "1":
            query_time = get_query_time()

            display_all_packages(
                package_table,
                trucks,
                query_time
            )

        elif choice == "2":
            try:
                package_id = int(
                    input("Enter package ID: ")
                )

                package = package_table.lookup(package_id)

                if package is not None:
                    query_time = get_query_time()

                    display_single_package(
                        package_table,
                        package_id,
                        query_time
                    )
                else:
                    print("Package not found.")

            except ValueError:
                print("Invalid package ID.")

        elif choice == "3":
            print("Exiting WGUPS Routing Program.")
            break

        else:
            print(
                "Invalid selection. "
                "Please enter 1, 2, or 3."
            )


if __name__ == "__main__":
    main()