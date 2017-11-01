from chvote.Types import VotingCard, Ballot, VoterBallot

def mpzconverter(o):
    if o.__class__.__name__ == 'mpz':
        return str(o)

    if isinstance(o, bytearray):
        return str(o)

    if isinstance(o, bytes):
        return str(o)

    from app.models.voterState import VoterState
    from app.models.electionAuthorityState import ElectionAuthorityState

    if isinstance(o, VoterState) or isinstance(o, ElectionAuthorityState) or isinstance(o, VotingCard) or isinstance(o, Ballot) or isinstance(o, VoterBallot):
        return o.__dict__