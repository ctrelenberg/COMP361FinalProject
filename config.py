import json

class Config:
    def __init__(self, config_file = 'config.json'):
        import os
        if os.path.isfile(config_file):
            self.conf = json.load(open('config.json', 'r'))
        else:
            self.conf = {}
        self.draw_edge_labels = self.get('draw_edge_labels', False)
        self.draw_node_labels = self.get('draw_node_labels', True)
        self.display_algorithm_indicator = self.get('display_algorithm_indicator', True)

    def get(self, string, default=None):
        return self.conf[string] if string in self.conf else default