
class Agent:
    """
    Based on the current game state decide what action to take
    """
    def __init__(self, params):
        self.params = params
    
    def step(self, game_state):
        dist, height, on_ground, score = game_state
        if height == self.params["dino_height"] and on_ground:
            return "crouch", self.params["crouch_time"]
        elif dist < (self.params["jump_dist"] + score*self.params["jump_dist_delta"]) and on_ground:
            return "jump", self.params["jump_time"]     
        return "",0