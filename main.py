import os
from VoteSimulation import VoteSimulation

def main():
    #level0test = ProtocolRunner(os.path.join("profiles","deterministic_level0.json"))
    #level0test.run(True, True)

    level3test = VoteSimulation(os.path.join("profiles","level3.json"))
    level3test.run(True, True)


if __name__ == '__main__':
    main()
