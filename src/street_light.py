from node import Node

class StreetLight(Node):
    def __init__(self, env, id, tx_range):
        super().__init__(env, id, tx_range)
        self.is_street_light = True
    
    def send_movement_alert(self, mpl_domain_address):
        # Implement MPL message sending logic
        print(f"Street Light {self.id} sending movement alert to MPL domain {mpl_domain_address}")

    def __str__(self):
        return f"Street Light {self.id}"