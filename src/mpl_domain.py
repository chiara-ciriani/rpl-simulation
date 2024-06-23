class MPL_Domain:
    def __init__(self, id, mpl_domain_address):
        self.id = id
        self.nodes = []
        self.mpl_domain_address = mpl_domain_address
        self.message_count = 0

    def add_node(self, node, verbose):
        if node not in self.nodes:
            self.nodes.append(node)
            node.mpl_domain = self
            if verbose: print(f"Node {node.id} added to MPL Domain {self.id}")

    def get_message_count(self):
        return self.message_count
    
    def increase_message_count(self):
        self.message_count += 1
    
    def __eq__(self, other):
        if isinstance(other, MPL_Domain):
            return self.id == other.id  
        return False

    def __str__(self):
        return f"MPL Domain {self.id} with address {self.mpl_domain_address} and nodes {[node.id for node in self.nodes]}"