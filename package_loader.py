# Assigns packages to delivery trucks while respecting
# package constraints and truck capacity.


def load_packages(trucks, package_table):
    # Packages with special delivery requirements are assigned first.

    # These packages must be delivered together.
    truck_1_required = [13, 14, 15, 16, 19, 20]

    # Priority packages assigned to the early truck so their
    # delivery deadlines can be met.
    truck_1_priority = [1, 29, 30, 31, 34, 37, 40]

    # Packages that must be on Truck 2 or are delayed until 9:05 AM.
    truck_2_required = [3, 6, 18, 25, 28, 32, 36, 38]

    # Package 9 must wait until its corrected address is available.
    truck_3_required = [9]

    # Assign packages with special constraints first.
    for package_id in truck_1_required + truck_1_priority:
        trucks[0].add_package(package_id)

    for package_id in truck_2_required:
        trucks[1].add_package(package_id)

    for package_id in truck_3_required:
        trucks[2].add_package(package_id)

    # Track all packages that have already been assigned.
    assigned = set()

    for truck in trucks:
        assigned.update(truck.packages)

    # Automatically assign all remaining packages to trucks
    # that still have available capacity.
    packages = package_table.get_all_packages()

    for package in sorted(packages, key=lambda p: p.package_id):
        package_id = package.package_id

        if package_id not in assigned:
            for truck in reversed(trucks):
                if truck.add_package(package_id):
                    assigned.add(package_id)
                    break