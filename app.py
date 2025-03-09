# app.py
# from flask import Flask, render_template, jsonify
# import math
# from ortools.constraint_solver import routing_enums_pb2
# from ortools.constraint_solver import pywrapcp

# app = Flask(__name__)

# def create_mysuru_data_model():
#     """Stores the data for the Mysuru bus stops routing problem."""
#     data = {}
#     # List of 13 bus stops in Mysuru (index 0 is the depot)
#     data["bus_stops"] = [
#         "Mysore Bus Station",   # Depot: Main bus terminal
#         "Mysore Junction",
#         "Gandhi Square",
#         "K.R. Circle",
#         "Mysore Palace",
#         "JLB Nagar",
#         "Vijayanagar",
#         "Kuvempu Nagar",
#         "Vidhyaranyapura",
#         "Lakshmipuram",
#         "Sultan's Park",
#         "Railway Station",
#         "Gokulam"
#     ]
    
#     # Hypothetical symmetric distance matrix (in km)
#     data["distance_matrix"] = [
#         [0,   2.0, 3.0, 2.5, 1.0, 3.5, 4.0, 4.5, 5.0, 3.0, 2.0, 2.5, 3.0],
#         [2.0, 0,   2.5, 1.5, 2.0, 3.0, 3.5, 4.0, 4.5, 3.0, 2.2, 2.8, 3.2],
#         [3.0, 2.5, 0,   2.0, 2.8, 3.2, 3.8, 4.3, 4.7, 3.5, 2.5, 3.0, 3.5],
#         [2.5, 1.5, 2.0, 0,   1.8, 2.5, 3.0, 3.8, 4.2, 2.8, 2.0, 2.5, 2.9],
#         [1.0, 2.0, 2.8, 1.8, 0,   3.0, 3.5, 4.0, 4.5, 3.2, 1.8, 2.2, 2.6],
#         [3.5, 3.0, 3.2, 2.5, 3.0, 0,   2.5, 3.2, 3.7, 2.5, 2.0, 2.8, 3.1],
#         [4.0, 3.5, 3.8, 3.0, 3.5, 2.5, 0,   2.2, 2.8, 3.0, 3.5, 3.8, 4.0],
#         [4.5, 4.0, 4.3, 3.8, 4.0, 3.2, 2.2, 0,   1.8, 2.5, 3.0, 3.4, 3.6],
#         [5.0, 4.5, 4.7, 4.2, 4.5, 3.7, 2.8, 1.8, 0,   2.0, 2.5, 2.9, 3.1],
#         [3.0, 3.0, 3.5, 2.8, 3.2, 2.5, 3.0, 2.5, 2.0, 0,   1.5, 2.0, 2.3],
#         [2.0, 2.2, 2.5, 2.0, 1.8, 2.0, 3.5, 3.0, 2.5, 1.5, 0,   1.5, 1.8],
#         [2.5, 2.8, 3.0, 2.5, 2.2, 2.8, 3.8, 3.4, 2.9, 2.0, 1.5, 0,   1.2],
#         [3.0, 3.2, 3.5, 2.9, 2.6, 3.1, 4.0, 3.6, 3.1, 2.3, 1.8, 1.2, 0]
#     ]
    
#     # Approximate (latitude, longitude) coordinates for each bus stop
#     data["coordinates"] = [
#         [12.3051, 76.6554],  # Mysore Bus Station
#         [12.3067, 76.6610],  # Mysore Junction
#         [12.3100, 76.6620],  # Gandhi Square
#         [12.3120, 76.6580],  # K.R. Circle
#         [12.3055, 76.6550],  # Mysore Palace
#         [12.3200, 76.6570],  # JLB Nagar
#         [12.3250, 76.6580],  # Vijayanagar
#         [12.3300, 76.6600],  # Kuvempu Nagar
#         [12.3350, 76.6620],  # Vidhyaranyapura
#         [12.3400, 76.6640],  # Lakshmipuram
#         [12.3450, 76.6660],  # Sultan's Park
#         [12.3500, 76.6680],  # Railway Station
#         [12.3550, 76.6700]   # Gokulam
#     ]
    
#     data["num_vehicles"] = 1
#     data["depot"] = 0
#     return data

# def solve_mysuru_tsp():
#     """Solves the TSP for Mysuru bus stops and returns the optimal route."""
#     data = create_mysuru_data_model()
#     manager = pywrapcp.RoutingIndexManager(len(data["bus_stops"]), data["num_vehicles"], data["depot"])
#     routing = pywrapcp.RoutingModel(manager)
#     distance_matrix = data["distance_matrix"]

#     def distance_callback(from_index, to_index):
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         # Multiply by 1000 to convert km to meters (to work with integer costs)
#         return int(distance_matrix[from_node][to_node] * 1000)

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

#     solution = routing.SolveWithParameters(search_parameters)
#     if solution:
#         route = []
#         total_distance = 0
#         index = routing.Start(0)
#         while not routing.IsEnd(index):
#             node = manager.IndexToNode(index)
#             route.append(node)
#             previous_index = index
#             index = solution.Value(routing.NextVar(index))
#             total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#         route.append(manager.IndexToNode(index))
#         return {
#             "route": route,
#             "total_distance": total_distance / 1000.0,  # Convert back to km
#             "bus_stops": data["bus_stops"],
#             "coordinates": data["coordinates"]
#         }
#     else:
#         return {
#             "route": [],
#             "total_distance": None,
#             "bus_stops": data["bus_stops"],
#             "coordinates": data["coordinates"]
#         }

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/solve")
# def solve():
#     result = solve_mysuru_tsp()
#     return jsonify(result)

# if __name__ == "__main__":
#     app.run(debug=True)
# from flask import Flask, render_template, jsonify
# import math
# from ortools.constraint_solver import routing_enums_pb2
# from ortools.constraint_solver import pywrapcp

# app = Flask(__name__)

# def compute_distance_matrix(coordinates):
#     """Computes a symmetric distance matrix (in km) from coordinates.
#     Uses a rough conversion (1 degree ~ 111 km) to compute Euclidean distance.
#     """
#     matrix = []
#     for i in range(len(coordinates)):
#         row = []
#         lat1, lon1 = coordinates[i]
#         for j in range(len(coordinates)):
#             if i == j:
#                 row.append(0)
#             else:
#                 lat2, lon2 = coordinates[j]
#                 # Euclidean distance multiplied by factor (111 km per degree) for rough conversion
#                 distance = math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111
#                 row.append(round(distance, 1))
#         matrix.append(row)
#     return matrix

# def create_mysuru_data_model():
#     """Stores the data for the extended Mysuru bus stops routing problem."""
#     data = {}
#     # Extended list of bus stops in Mysuru (index 0 is the depot)
#     data["bus_stops"] = [
#         "Mysore Bus Station",   # Depot: Main bus terminal
#         "Mysore Junction",
#         "Gandhi Square",
#         "K.R. Circle",
#         "Mysore Palace",
#         "JLB Nagar",
#         "Vijayanagar",
#         "Kuvempu Nagar",
#         "Vidhyaranyapura",
#         "Lakshmipuram",
#         "Sultan's Park",
#         "Railway Station",
#         "Gokulam",
#         "Hebbal",
#         "Hinkal",
#         "Karanji",
#         "Chamundi Hills",
#         "Amarapuri",
#         "Naganahalli",
#         "Nanjangud Road"
#     ]
    
#     # Approximate (latitude, longitude) coordinates for each bus stop.
#     # The first 13 are central stops; the remaining are on the outskirts.
#     data["coordinates"] = [
#         [12.3051, 76.6554],  # Mysore Bus Station
#         [12.3067, 76.6610],  # Mysore Junction
#         [12.3100, 76.6620],  # Gandhi Square
#         [12.3120, 76.6580],  # K.R. Circle
#         [12.3055, 76.6550],  # Mysore Palace
#         [12.3200, 76.6570],  # JLB Nagar
#         [12.3250, 76.6580],  # Vijayanagar
#         [12.3300, 76.6600],  # Kuvempu Nagar
#         [12.3350, 76.6620],  # Vidhyaranyapura
#         [12.3400, 76.6640],  # Lakshmipuram
#         [12.3450, 76.6660],  # Sultan's Park
#         [12.3500, 76.6680],  # Railway Station
#         [12.3550, 76.6700],  # Gokulam
#         [12.3600, 76.6720],  # Hebbal (Outskirts)
#         [12.3650, 76.6740],  # Hinkal (Outskirts)
#         [12.3700, 76.6760],  # Karanji (Outskirts)
#         [12.4100, 76.6800],  # Chamundi Hills (Outskirts)
#         [12.3150, 76.6800],  # Amarapuri (Outskirts)
#         [12.3200, 76.6850],  # Naganahalli (Outskirts)
#         [12.3300, 76.6900]   # Nanjangud Road (Outskirts)
#     ]
    
#     # Dynamically compute the distance matrix from coordinates.
#     data["distance_matrix"] = compute_distance_matrix(data["coordinates"])
    
#     data["num_vehicles"] = 1
#     data["depot"] = 0
#     return data

# def solve_mysuru_tsp():
#     """Solves the TSP for Mysuru bus stops and returns the optimal route."""
#     data = create_mysuru_data_model()
#     manager = pywrapcp.RoutingIndexManager(len(data["bus_stops"]), data["num_vehicles"], data["depot"])
#     routing = pywrapcp.RoutingModel(manager)
#     distance_matrix = data["distance_matrix"]

#     def distance_callback(from_index, to_index):
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         # Multiply by 1000 to convert km to meters (to work with integer costs)
#         return int(distance_matrix[from_node][to_node] * 1000)

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

#     solution = routing.SolveWithParameters(search_parameters)
#     if solution:
#         route = []
#         total_distance = 0
#         index = routing.Start(0)
#         while not routing.IsEnd(index):
#             node = manager.IndexToNode(index)
#             route.append(node)
#             previous_index = index
#             index = solution.Value(routing.NextVar(index))
#             total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#         route.append(manager.IndexToNode(index))
#         return {
#             "route": route,
#             "total_distance": total_distance / 1000.0,  # Convert back to km
#             "bus_stops": data["bus_stops"],
#             "coordinates": data["coordinates"]
#         }
#     else:
#         return {
#             "route": [],
#             "total_distance": None,
#             "bus_stops": data["bus_stops"],
#             "coordinates": data["coordinates"]
#         }

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/solve")
# def solve():
#     result = solve_mysuru_tsp()
#     return jsonify(result)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, jsonify
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

app = Flask(__name__)

def compute_distance_matrix(coordinates):
    """
    Computes a symmetric distance matrix (in km) from latitude/longitude coordinates.
    Uses a rough conversion factor: 1 degree ~ 111 km.
    """
    matrix = []
    for i in range(len(coordinates)):
        row = []
        lat1, lon1 = coordinates[i]
        for j in range(len(coordinates)):
            if i == j:
                row.append(0)
            else:
                lat2, lon2 = coordinates[j]
                # Euclidean distance in degrees, then convert to km
                distance = math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111
                row.append(round(distance, 1))
        matrix.append(row)
    return matrix

def create_mysuru_data_model():
    """Stores the extended data for the Mysuru (and beyond) bus stops routing problem."""
    data = {}
    # Extended list of bus stops.
    # The first 20 stops are within/around Mysuru,
    # while stops 20+ are in other parts of Karnataka to ensure a long route.
    data["bus_stops"] = [
        "Mysore Bus Station",      # 0: Depot
        "Mysore Junction",         # 1
        "Gandhi Square",           # 2
        "K.R. Circle",             # 3
        "Mysore Palace",           # 4
        "JLB Nagar",               # 5
        "Vijayanagar",             # 6
        "Kuvempu Nagar",           # 7
        "Vidhyaranyapura",         # 8
        "Lakshmipuram",            # 9
        "Sultan's Park",           # 10
        "Railway Station",         # 11
        "Gokulam",                 # 12
        "Hebbal",                  # 13
        "Hinkal",                  # 14
        "Karanji",                 # 15
        "Chamundi Hills",          # 16
        "Amarapuri",               # 17
        "Naganahalli",             # 18
        "Nanjangud Road",          # 19
        # Additional stops across Karnataka:
        "Bangalore City Center",           # 20
        "Bangalore Intl Airport",          # 21
        "Hubli Bus Terminal",              # 22
        "Mangalore Port",                  # 23
        "Belgaum Central",                 # 24
        "Gulbarga Station",                # 25
        "Davangere Hub",                   # 26
        "Bellary Depot",                   # 27
        "Shimoga Station",                 # 28
        "Tumkur Main Terminal",            # 29
        "Chitradurga Center",              # 30
        "Coorg Tourist Bus Stop",          # 31
        "Mysore Outer Ring Road",          # 32
        "Mandya Town",                     # 33
        "Krishnarajapuram",                # 34
        "Davangere Outskirts"              # 35
    ]
    
    # Approximate coordinates for each stop.
    # The first 20 are around Mysuru; the rest are based on approximate locations in Karnataka.
    data["coordinates"] = [
        [12.3051, 76.6554],  # Mysore Bus Station
        [12.3067, 76.6610],  # Mysore Junction
        [12.3100, 76.6620],  # Gandhi Square
        [12.3120, 76.6580],  # K.R. Circle
        [12.3055, 76.6550],  # Mysore Palace
        [12.3200, 76.6570],  # JLB Nagar
        [12.3250, 76.6580],  # Vijayanagar
        [12.3300, 76.6600],  # Kuvempu Nagar
        [12.3350, 76.6620],  # Vidhyaranyapura
        [12.3400, 76.6640],  # Lakshmipuram
        [12.3450, 76.6660],  # Sultan's Park
        [12.3500, 76.6680],  # Railway Station
        [12.3550, 76.6700],  # Gokulam
        [12.3600, 76.6720],  # Hebbal
        [12.3650, 76.6740],  # Hinkal
        [12.3700, 76.6760],  # Karanji
        [12.4100, 76.6800],  # Chamundi Hills
        [12.3150, 76.6800],  # Amarapuri
        [12.3200, 76.6850],  # Naganahalli
        [12.3300, 76.6900],  # Nanjangud Road
        [12.9716, 77.5946],  # Bangalore City Center
        [13.1986, 77.7066],  # Bangalore Intl Airport
        [15.3617, 75.1240],  # Hubli Bus Terminal
        [12.9141, 74.8550],  # Mangalore Port
        [16.8460, 74.4977],  # Belgaum Central
        [17.3291, 76.8343],  # Gulbarga Station
        [14.4671, 75.9219],  # Davangere Hub
        [15.1394, 76.9214],  # Bellary Depot
        [13.9299, 75.5681],  # Shimoga Station
        [13.3389, 77.1012],  # Tumkur Main Terminal
        [14.3195, 76.4171],  # Chitradurga Center
        [12.5621, 75.9336],  # Coorg Tourist Bus Stop
        [12.4000, 76.7500],  # Mysore Outer Ring Road
        [12.5241, 76.8958],  # Mandya Town
        [12.9333, 77.5500],  # Krishnarajapuram
        [14.5000, 75.9000]   # Davangere Outskirts
    ]
    
    # Compute the distance matrix based on the coordinates.
    data["distance_matrix"] = compute_distance_matrix(data["coordinates"])
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data

def solve_mysuru_tsp():
    """Solves the TSP for the extended bus stops and returns the optimal route."""
    data = create_mysuru_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data["bus_stops"]), data["num_vehicles"], data["depot"])
    routing = pywrapcp.RoutingModel(manager)
    distance_matrix = data["distance_matrix"]

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # Multiply by 1000 to convert km to meters (for integer costs)
        return int(distance_matrix[from_node][to_node] * 1000)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        route = []
        total_distance = 0
        index = routing.Start(0)
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        route.append(manager.IndexToNode(index))
        return {
            "route": route,
            "total_distance": total_distance / 1000.0,  # Convert back to km
            "bus_stops": data["bus_stops"],
            "coordinates": data["coordinates"]
        }
    else:
        return {
            "route": [],
            "total_distance": None,
            "bus_stops": data["bus_stops"],
            "coordinates": data["coordinates"]
        }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve")
def solve():
    result = solve_mysuru_tsp()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
