class FlightInfo:
    
    def __init__(self, departure_time, arrival_time, full_price, taxes, departure_port, arrival_port, connection_port):
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.full_price = full_price
        self.departure_port = departure_port
        self.arrival_port = arrival_port
        self.connection_port = connection_port
        self.taxes = taxes
    
    def __str__(self):
        return "flight info {"+"\n\tdeparture port: {}\n\tarrival port: {}\n\tconnection port: {}\n\tdeparture time {}\n\tarrival time: {}\n\tfull price: {}\n\ttaxes: {}\n".format(self.departure_port, self.arrival_port, self.connection_port, self.departure_time, self.arrival_time, self.full_price, self.taxes) + "}"