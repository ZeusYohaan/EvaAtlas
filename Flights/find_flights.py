from fast_flights import FlightData, Passengers, Result, get_flights, search_airport


def get_flights_google(adults, children, seat_class, date, dep_airport, arr_airport):
    departure_airport = search_airport(dep_airport)[0]
    arrival_airport = search_airport(arr_airport)[0]

    result: Result = get_flights(
        flight_data=[
            FlightData(date=date, from_airport=departure_airport, to_airport=arrival_airport)
        ],

        trip="one-way",
        seat=seat_class,
        passengers=Passengers(adults=adults, children=children, infants_in_seat=0, infants_on_lap=0),
        fetch_mode="fallback",
    )
    return result.flights


print(get_flights_google(1, 0, "economy", "2025-12-03", "Heathrow", "Haneda"))
