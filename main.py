import os
from ProtocolRunner         import ProtocolRunner

def main():

    level0test = ProtocolRunner(os.path.join("profiles","deterministic_level0.json"))
    level0test.run(False, True)

if __name__ == '__main__':
    main()
