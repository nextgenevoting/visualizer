import os
from VoteSimulation import VoteSimulation

def main():
    level3test = VoteSimulation(os.path.join("profiles","default.json"))
    level3test.run(True, True)


if __name__ == '__main__':
    main()
