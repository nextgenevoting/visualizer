from chvote.Types import VotingCard

def mpzconverter(o):
    if o.__class__.__name__ == 'mpz':
        return str(o)

    if isinstance(o, bytearray):
        return str(o)

    if isinstance(o, bytes):
        return str(o)


    if isinstance(o, VotingCard):
        return o.__dict__