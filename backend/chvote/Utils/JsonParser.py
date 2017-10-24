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

    from app.models.voterState import VoterState
    from app.models.electionAuthorityState import ElectionAuthorityState

    if isinstance(o, VoterState) or isinstance(o, ElectionAuthorityState):
        return o.__dict__