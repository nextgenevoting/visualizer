import os
from VoteSimulation import VoteSimulation

def main():
    automatic = True
    verbose = True
    simulation = VoteSimulation(os.path.join("profiles", "default.json"))
    simulation.run(automatic, verbose)

if __name__ == '__main__':
    main()
