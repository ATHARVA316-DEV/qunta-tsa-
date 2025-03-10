# Mysuru Bus Routing Optimization

## Overview
This project implements a Traveling Salesman Problem (TSP) solution for optimizing bus routes in Mysuru, India. It uses Google's OR-Tools to compute the shortest possible route for visiting multiple bus stops efficiently.

## Features
- Computes optimal routes for a given set of bus stops.
- Uses OR-Tools for solving the TSP.
- Flask web server to serve the optimized route as a JSON API.
- Supports an extended list of locations, including additional Karnataka destinations.
- Computes Euclidean distance matrix based on geographical coordinates.

## Technologies Used
- Python
- Flask
- OR-Tools (Google's Optimization Tools)
- HTML, JavaScript (for the front-end visualization, if applicable)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/mysuru-bus-routing.git
   cd mysuru-bus-routing
   ```
2. Install dependencies:
   ```sh
   pip install flask ortools
   ```

## Usage
1. Run the Flask application:
   ```sh
   python app.py
   ```
2. Open a web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```
3. Use the `/solve` API endpoint to get the optimized route:
   ```sh
   curl http://127.0.0.1:5000/solve
   ```

## API Endpoints
- `GET /` - Returns the home page (if front-end is implemented).
- `GET /solve` - Solves the TSP and returns the optimal route in JSON format.

## Example JSON Response
```json
{
  "route": [0, 3, 5, 7, 10, 12, 2, 1, 6, 4, 8, 9, 11],
  "total_distance": 12.5,
  "bus_stops": ["Mysore Bus Station", "Mysore Junction", "Gandhi Square", ...],
  "coordinates": [[12.3051, 76.6554], [12.3067, 76.6610], ...]
}
```

## Future Enhancements
- Front-end visualization of routes using Google Maps or Leaflet.
- Quantum Computing approach using Qiskit for solving TSP.
- Dynamic real-time traffic data integration.

## License
This project is licensed under the MIT License.
