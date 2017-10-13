def GetVotingCard(v, V_bold, w_bold, c_bold, n_bold, k_bold, X_bold, Y_bold, FC_bold, rc_bold):
    """
    Algorithm 7.14: Computes a string S ∈ A*_ucs, which represents a code sheet
    that can be printed on paper and sent to voter v.

    Args:
        v (int):         Voter index
        V_bold (string): Voter description
        w_bold (list):   Counting circles
        c_bold (list):   List of candidate descriptions
        n_bold (int):    Number of candidated
        k_bold (int):    Number of selections
        X_bold (...):    Voting code
        Y_bold (...):    Confirmation code
        FC_bold (...):   Finalization code
        rc_bold (...):   Verification codes

    Returns:
        string:     code sheet
    """

    # TODO

    S = \
    """
VotingCard for voter {v}: {V}
---------------------------------------------------
Candidates: [{c}]
Selections: {k}
Voting code: {X}
Confirmation code: {Y}
Finalization code: {FC}
Verification codes:
    {rc}
    """.format(
          v =  v
        , V =  V_bold
        , c = ', '.join(c_bold)
        , n = n_bold
        , k = k_bold
        , X = X_bold
        , Y = Y_bold
        , FC = FC_bold
        , rc = '\n\t'.join(rc_bold)
    )

    return S
