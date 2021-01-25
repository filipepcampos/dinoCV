import datetime
import time

class Logger:
    def __init__(self, file):
        self.file = file
        
    def log_start(self, params):
        with open(self.file, "a") as file:
            now = datetime.datetime.now()
            file.write("\n")
            file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
            file.write(f"\n params: {params}\n")
    
    def log_score(self, score):
        with open(self.file, "a") as file:
            file.write(f" final_score: {score}\n")