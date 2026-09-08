# HashTable stores WGUPS packages using the package ID as the key.
# Separate chaining is used to handle collisions between package IDs.

class HashTable:
    def __init__(self, capacity=40):
        self.table = []

        for _ in range(capacity):
            self.table.append([])

    # Inserts a package into the hash table using its package ID as the key.
    def insert(self, package_id, package):
        bucket_index = package_id % len(self.table)
        bucket = self.table[bucket_index]

        for item in bucket:
            if item[0] == package_id:
                item[1] = package
                return

        bucket.append([package_id, package])

    # Searches for a package by its package ID and returns the Package object.
    def lookup(self, package_id):
        bucket_index = package_id % len(self.table)
        bucket = self.table[bucket_index]

        for item in bucket:
            if item[0] == package_id:
                return item[1]

        return None

    # Returns all packages currently stored in the hash table.
    def get_all_packages(self):
        packages = []

        for bucket in self.table:
            for item in bucket:
                packages.append(item[1])

        return packages