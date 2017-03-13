def GetSheet(i, V, c, n, k, X, Y, FC, rc):
    """
    Algorithm 7.14: Computes a string S ∈ A*_ucs, which represents a code sheet
    that can be printed on paper and sent to voter i.

    Args:
        i (int):    Voter index
        V (string): Voter description
        c (list):   List of candidate descriptions
        n (int):    Number of candidated
        k (int):    Number of selections
        X (...):    Voting code
        Y (...):    Confirmation code
        FC (...):   Finalization code
        rc (...):   Return codes

    Returns:
        string:     code sheet
    """

    # TODO
    S = \
    """
    Voter {i}: {V}

    Finalization code: {FC}
    """.format(
        { 'i':  i
        , 'V':  V
        , 'c':  c
        , 'n':  n
        , 'k':  k
        , 'X':  X
        , 'Y':  Y
        , 'FC': FC
        , 'rc': rc
        }
    )

    return S
