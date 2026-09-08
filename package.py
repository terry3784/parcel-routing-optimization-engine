from datetime import timedelta

# Package class represents an individual delivery package.
# Each Package object stores the package's delivery information
# and tracks its status as it moves through the delivery process.

class Package:
    def __init__(self, package_id, address, city, state, zip_code,
                 deadline, weight, notes):

        # Store package information loaded from the package data.
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes

        # All packages begin at the hub and do not have departure
        # or delivery times until the delivery simulation runs.
        self.status = "At Hub"
        self.departure_time = None
        self.delivery_time = None

    # Returns the package status at a specific time.
    def get_status_at_time(self, query_time):
        delayed_packages = [6, 25, 28, 32]
        delayed_until = timedelta(hours=9, minutes=5)

        # Delayed packages do not arrive at the hub until 9:05 AM.
        if self.package_id in delayed_packages and query_time < delayed_until:
            return "Delayed"

        if self.departure_time is None or query_time < self.departure_time:
            return "At Hub"

        if self.delivery_time is None or query_time < self.delivery_time:
            return "En Route"

        return "Delivered"

    # Returns Package 9's address information based on the query time.
    # The corrected address does not become available until 10:20 AM.
    def get_address_at_time(self, query_time):
        if self.package_id == 9 and query_time < timedelta(hours=10, minutes=20):
            return "300 State St", "Salt Lake City", "UT", "84103"

        return self.address, self.city, self.state, self.zip_code