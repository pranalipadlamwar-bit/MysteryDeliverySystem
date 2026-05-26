



# Import required modules
import json
import math
import random
import csv


# Function to calculate Euclidean distance
def distance(point1, point2):
    return math.sqrt(
        (point2[0] - point1[0]) ** 2 +
        (point2[1] - point1[1]) ** 2
    )


# Read JSON data from file
filename = input("Enter test case file name: ")

with open(filename, "r") as file:
    data = json.load(file)



# Extract data
warehouses = data["warehouses"]
agents = data["agents"]
packages = data["packages"]


# Create report dictionary
report = {}

for agent in agents:
    report[agent] = {
        "packages_delivered": 0,
        "total_distance": 0,
        "delivered_packages": [],
        "total_delay": 0
    }


# Start package assignment
for package in packages:

    # Get warehouse information
    warehouse_name = package["warehouse"]
    warehouse_location = warehouses[warehouse_name]

    # Variables to find nearest agent
    nearest_agent = None
    shortest_distance = float("inf")

    # Find nearest agent to warehouse
    for agent, agent_location in agents.items():

        d = distance(agent_location, warehouse_location)

        if d < shortest_distance:
            shortest_distance = d
            nearest_agent = agent

    # Get package destination
    destination = package["destination"]

    # Distance from warehouse to destination
    warehouse_to_destination = distance(
        warehouse_location,
        destination
    )

    # Total travel distance
    total_trip = shortest_distance + warehouse_to_destination

    # BONUS: Random delivery delay
    delay = random.randint(1, 10)

    # Update report
    report[nearest_agent]["packages_delivered"] += 1

    report[nearest_agent]["total_distance"] += total_trip

    report[nearest_agent]["total_delay"] += delay

    # Store delivered package IDs
    report[nearest_agent]["delivered_packages"].append(
        package["id"]
    )

    # BONUS: ASCII route visualization
    print("\nDelivery Route")
    print(
        nearest_agent,
        "--->",
        warehouse_name,
        "--->",
        destination
    )

    print("Delay:", delay, "minutes")


# Calculate efficiency
for agent in report:

    packages_delivered = report[agent]["packages_delivered"]

    total_distance = report[agent]["total_distance"]

    # Efficiency formula
    if total_distance > 0:
        efficiency = (
            packages_delivered / total_distance
        ) * 100
    else:
        efficiency = 0

    # Round values
    report[agent]["efficiency"] = round(efficiency, 2)

    report[agent]["total_distance"] = round(
        total_distance,
        2
    )


# Find best agent
best_agent = max(
    report,
    key=lambda a: report[a]["efficiency"]
)

report["best_agent"] = best_agent


# Print final report
print("\nFINAL REPORT")
print(json.dumps(report, indent=4))


# Save report to JSON file
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)


# BONUS: Export best agent to CSV
with open("top_performer.csv", "w", newline="") as file:

    writer = csv.writer(file)

    # CSV headings
    writer.writerow([
        "Agent",
        "Packages Delivered",
        "Total Distance",
        "Efficiency"
    ])

    # Best agent data
    writer.writerow([
        best_agent,
        report[best_agent]["packages_delivered"],
        report[best_agent]["total_distance"],
        report[best_agent]["efficiency"]
    ])


print("\nTop performer exported to top_performer.csv")
