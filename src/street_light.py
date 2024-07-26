from message import Message
from node import Node

class StreetLight(Node):
    def __init__(self, env, id, x, y, tx_range, mpl_domain_address=None):
        super().__init__(env, id, x, y, tx_range)
        self.is_street_light = True
        self.turn_on = False
        self.mpl_domain_address_1 = mpl_domain_address
        self.mpl_domain_address_2 = None
        self.mpl_domain_address_3 = None
        self.track = None
        self.track2 = None
    
    def send_movement_alert(self, domain_address, verbose):
        if verbose: print(f"Street Light {self.id} sending movement alert to MPL domain {domain_address}")
        message = Message(self.id, domain_address, "MPL Alert")
        self.forward_message(message, domain_address, verbose)
        return message

    def forward_message(self, message, domain_address, verbose):
        if message.get_destination() == domain_address and not self.turn_on:
            self.turn_on = True
            if verbose: print(f"Street Light {self.id} turned ON due to MPL message.")
        super().forward_message(message, domain_address, verbose)

    def __str__(self):
        return f"Street Light {self.id}"
    
    def install_track(self, track, verbose):
        if not self.track:
            self.track = track
        else:
            self.track2 = track

        if verbose:
            print(f"Street light {self.id} track:\n")
            if not self.track2:
                print(self.track)    
            else:
                print(self.track2)
    
    def send_message_through_track(self, target):
        return self.track.send_message_through_track(target)

    def send_message_through_track2(self, target):
        return self.track2.send_message_through_track(target)
    
    def add_mpl_domain_address_1(self, mpl_domain_address_1):
        self.mpl_domain_address_1 = mpl_domain_address_1
    
    def add_mpl_domain_address_2(self, mpl_domain_address_2):
        self.mpl_domain_address_2 = mpl_domain_address_2