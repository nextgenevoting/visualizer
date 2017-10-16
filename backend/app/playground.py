from app.parties.BulletinBoard import BulletinBoard
from app.voteSimulator import VoteSimulator
from app.database import db, saveComplex
from app.models.bulletinBoardState import BulletinBoardState
from app.models.electionAuthorityState import  ElectionAuthorityState

if __name__ == '__main__':
    if 1==0:
        id = db.elections.insert({'title': "Testelection"})

        newBBState = BulletinBoardState(str(id))
        db.bulletinBoardStates.insert({'election': str(id), 'state': saveComplex(newBBState)})
        for j in range(3):
            newAuthState = ElectionAuthorityState(j)
            db.electionAuthorityStates.insert({'election': str(id), 'authorityID':j, 'state': saveComplex(newAuthState)})

    id = "59e332b65c926214346b994c"
    sim = VoteSimulator(str(id))

    sim.bulletinBoard.state.voters = [1,2,3]
    sim.authorities[0].state.points.append(1)
    sim.authorities[1].state.points.append(2)
    sim.authorities[2].state.points.append(3)
    sim.persist()

    sim2 = VoteSimulator(str(id))

    print("done")