# -*- coding: utf-8 -*-

m = 160 # 160bits

def member_ll(id, A, B): # A < id < B
    if A == B: # ノード数が1しかないときの例外処理
        return True
    elif A > B: # リングネットワークの周回境界条件
        B2  = B + 2**m
        id2 = id + 2**m
        if A < id:
            return A < id < B2
        else:
            return A < id2 < B2
    else:
        return A < id < B

def member_el(id, A, B): # A <= id < B
    if A == B: # ノード数が1しかないときの例外処理
        return True
    elif A == id:
        return True
    elif A > B: # リングネットワークの周回境界条件
        B2  = B + 2**m
        id2 = id + 2**m
        if A < id:
            return A <= id < B2
        else:
            return A <= id2 < B2
    else:
        return A <= id < B

def member_le(id, A, B): # A < id <= B
    if A == B: # ノード数が1しかないときの例外処理
        return True
    elif B == id:
        return True
    elif A > B: # リングネットワークの周回境界条件
        B2  = B + 2**m
        id2 = id + 2**m
        if A < id:
            return A < id <= B2
        else:
            return A < id2 <= B2
    else:
        return A < id <= B
