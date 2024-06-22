from message import Message
from node import Node

class StreetLight(Node):
    def __init__(self, env, id, tx_range, mpl_domain_address=None):
        super().__init__(env, id, tx_range)
        self.is_street_light = True
        self.turn_on = False
        self.mpl_domain_address = mpl_domain_address
        self.track = None
    
    def send_movement_alert(self):
        print(f"Street Light {self.id} sending movement alert to MPL domain {self.mpl_domain_address}")
        message = Message(self.id, self.mpl_domain_address, "MPL Alert")
        self.forward_message(message)
        return message

    def forward_message(self, message):
        if message.get_destination() == self.mpl_domain_address and not self.turn_on:
            self.turn_on = True
            print(f"Street Light {self.id} turned ON due to MPL message.")
        super().forward_message(message)

    def __str__(self):
        return f"Street Light {self.id}"
    
    def install_track(self, track):
        self.track = track

        print(f"Street light {self.id} track:\n")
        print(self.track)
    
    def send_message_through_track(self, target):
        return self.track.send_message_through_track(target)