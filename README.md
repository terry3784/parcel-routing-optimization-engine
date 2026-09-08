# Logistics Routing & Dispatch Optimization Engine

A discrete-event delivery routing and package tracking simulation built in pure Python. The system models multi-vehicle delivery constraints, dynamic package status updates, real-time address redirections, and vehicle scheduling using a greedy nearest-neighbor graph heuristic and a custom direct-chaining hash table.

---

## Key Features

- **Custom Hash Table Implementation:** Stores and queries delivery packages in $O(1)$ average time complexity using direct chaining for collision resolution, avoiding reliance on built-in dictionary primitives.
- **Constrained Route Optimization:** Solves a multi-vehicle routing problem under real-world logistics constraints:
  - Strict delivery deadlines (e.g., morning commitments).
  - Truck capacity limits (max 16 packages per truck).
  - Inter-package delivery bundling requirements.
  - Driver availability constraints (2 drivers operating 3 vehicles).
  - Delayed package arrivals and dynamic mid-route address corrections.
- **Discrete Event Timeline Simulator:** Accurately models vehicle departure, transit time at fixed speed (18 mph), and arrival times, allowing point-in-time state reconstruction for any package or vehicle.
- **Interactive CLI Query Interface:** Allows operators to inspect full fleet statuses or lookup specific package data at any chosen timestamp.

---

## System Architecture

```text
├── data_loader.py       # Ingests and parses raw package CSV records (ETL)
├── distance_loader.py   # Extracts two-dimensional symmetric distance matrix
├── hash_table.py        # Custom chaining hash table implementation
├── main.py              # Application entry point and interactive CLI
├── package.py           # Package domain entity and state evaluation logic
├── package_loader.py    # Constraint-based initial load heuristic
├── routing.py           # Nearest-neighbor routing algorithm and distance accumulation
├── truck.py             # Truck vehicle entity tracking speed, mileage, and clock
├── distances.csv        # Location distance matrix
└── packages.csv         # Raw manifest records
```
---

## Algorithmic Complexity

- **Hash Table Lookup / Insertion:**
  - Average Case: $O(1)$
  - Worst Case (Collision Chain): $O(N)$
- **Nearest-Neighbor Routing:**
  - Given $N$ packages on a truck, evaluating candidates for the next closest stop runs in $O(N)$ per stop, resulting in an overall routing complexity of $O(N^2)$ with $O(N)$ auxiliary space.

---

## Getting Started

### Prerequisites

- Python 3.8+ (No third-party dependencies required; uses Python standard library).

### Installation & Execution

1. Clone this repository:

```bash
git clone https://github.com/terry3784/parcel-routing-optimization-engine.git
cd parcel-routing-optimization-engine
```

2. Execute the program:

```bash
python main.py
```

3. Use the interactive CLI by choosing option 1, 2, or 3.