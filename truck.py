# Represents a delivery truck and tracks its packages,
# location, mileage, departure time, and current simulation time.
class Truck:
    def __init__(self, truck_id, departure_time):
        self.truck_id = truck_id
        self.departure_time = departure_time

        # Each truck begins at the hub.
        self.current_location = 0

        # Packages assigned to this truck will be stored by package ID.
        self.packages = []

        # Maximum number of packages the truck can carry.
        self.capacity = 16

        # Trucks begin with zero miles traveled.
        self.mileage = 0.0

        # The truck's clock begins at its departure time.
        self.current_time = departure_time

        # WGUPS trucks travel at an average speed of 18 mph.
        self.speed = 18.0

    # Returns True if the truck still has room for another package.
    def has_capacity(self):
        return len(self.packages) < self.capacity

    # Adds a package to the truck if capacity is available.
    def add_package(self, package_id):
        if self.has_capacity():
            self.packages.append(package_id)
            return True

        return False