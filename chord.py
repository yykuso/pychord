# -*- coding: utf-8 -*-
import hashlib
import random
from member import *

m = 160 # 160bits

# Node()の管理の手伝いをするクラス
# 後のノードの離脱の実装を考慮して実装しておいた
# ノードの接続情報の更新についてはNode()でしか行わない
class Network():
    def __init__(self):
        self.node = []
        self.join_list = {}

    # ランダムにノードを指定して，そこの対してjoinする(同時に単一ノードしか参加できない)
    def single_join(self, node_num):
        node = Node(node_num)
        if len(self.join_list) == 0:
            node.single_join(node)
            self.node.append(node)
            self.join_list[node_num] = node_num
        else:
            rand_num = random.choice(self.join_list.keys())
            node.single_join(self.node[rand_num])
            self.node.append(node)
            self.join_list[node_num] = node_num

    # Stabilize利用で複数のノードが同時に参加することができるバージョン
    def multi_join(self, node_num):
        node = Node(node_num)
        if len(self.join_list) == 0:
            node.multi_join(node)
            self.node.append(node)
            self.join_list[node_num] = node_num
        else:
            rand_num = random.choice(self.join_list.keys())
            node.multi_join(self.node[rand_num])
            self.node.append(node)
            self.join_list[node_num] = node_num

    # 時間経過によってStabilize処理がされてゆく様を表現
    def time_elapsed(self, time):
        for i in range(time):
            rand_num = random.choice(self.join_list.keys())
            temp = self.node[rand_num]

            if random.randint(0,1) == 1:
                temp.stabilize()
            else:
                temp.fix_fingers()

    def info(self):
        for index, item in enumerate(self.node):
            item.info_node()

    def info_connecton(self):
        for index, item in enumerate(self.node):
            item.info_connecton()

    def check_ring(self):
        rand_num = random.choice(self.join_list.keys())
        res1 = self.node[rand_num].check_successor(MAXSTACK=len(self.node))
        if res1 != len(self.node) and res1 != -1:
            print "Some nodes are not participating in Chord Network"
        res2 = self.node[rand_num].check_predecessor(MAXSTACK=len(self.node))
        if res2 != len(self.node) and res2 != -1:
            print "Some nodes are not participating in Chord Network"



# ノードの接続等を行うChord Networkの根幹部分
# 基本は論文中の擬似コードと同様の動き
class Node():
    def __init__(n, IP):
        n.ip = IP
        n.id = long(hashlib.sha1(str(IP)).hexdigest(),16)
        # machine ID is [0, 2^160-1] b/c sha-1 is 160bits
        n.finger = {} # = n.finger[k] 論文でいうと finger[k]  の部分
        n.start  = {} # = n.start[k]  論文でいうと finger[k].start の部分
        for k in range(1,m+1):
            n.start[k] = (n.id + 2**(k-1)) % (2**m)

    ## nの担当するidのSuccessorを探す
    def find_successor(n, id):
        # print "    find_successor    id:", hex(id)
        nn = n.find_predecessor(id)
        return nn.successor()

    ## nの担当するidのPredecessorを探す
    def find_predecessor(n, id):
        # print "    find_predecessor    id:", hex(id)
        nn = n
        while not member_le(id,nn.id,nn.successor().id):
            nn = nn.closest_preceding_finger(id)
        return nn

    ## idの直前のfingerを返す
    def closest_preceding_finger(n,id):
        # print "      closest_preceding_finger    id:", hex(id)
        for i in range(m,0,-1):
            if member_ll(n.finger[i].id, n.id, id):
                return n.finger[i]
        return n

    ## #define successor finger[1]
    def successor(n):
        return n.finger[1]

    ## ノードnがネットワークに参加する（ネットワーク内の任意のノードnn）
    def single_join(n, nn):
        if n != nn:
            # print "more join   IP:", n.ip
            n.init_finger_table(nn)
            n.update_others()
        else: # nnがネットワーク内で唯一ノードであれば
            # print "first join   IP:", n.ip
            for i in range(1,m+1):
                n.finger[i] = n
            n.predecessor = n

    ## ノードnのFingerTableを初期化
    def init_finger_table(n, nn):
        # print "  init_finger_table"
        n.finger[1] = nn.find_successor(n.start[1])
        n.predecessor = n.successor().predecessor
        n.successor().predecessor = n
        for i in range(1,m):
            if member_el(n.start[i+1], n.id, n.finger[i].id):
                n.finger[i+1] = n.finger[i]
            else:
                n.finger[i+1] = nn.find_successor(n.start[i+1])

    ## FingerTableがnに参照すべき全ノードを更新する
    def update_others(n):
        # print "  update_others"
        for i in range(1,m+1):
            # i番目のfingerがnである可能性の直前ノードpを見つける
            if 2**(i-1) <= n.id: # リングネットワークの周回境界条件
                p = n.find_predecessor(n.id - 2**(i-1))
            else:
                p = n.find_predecessor(2**m + n.id - 2**(i-1))
            p.update_finger_table(n,i)

    ## ノードsがノードnのi番目のfingerであれば，nのFingerTableをsで更新する
    def update_finger_table(n, s, i):
        # print "    update_finger_table"
        if member_ll(s.id, n.id, n.finger[i].id):
            n.finger[i] = s
            p = n.predecessor # nの直前ノードを得る
            p.update_finger_table(s,i)


    ## node joinが単体でない場合の対応
    def multi_join(n, nn):
        if n != nn:
            # print "multi join   IP:", n.ip
            n.predecessor = None
            n.finger[1] = nn.find_successor(n.id)
            n.init_finger_table(nn) # 追加
        else: # nnがネットワーク内で唯一ノードであれば
            # print "first multi join   IP:", n.ip
            for i in range(1,m+1):
                n.finger[i] = n
            n.predecessor = n

    ## ノードnの直前のSuccesorを定期的に確認して，nについてSuccesorに伝える
    def stabilize(n):
        x = n.successor().predecessor
        if member_ll(x.id, n.id, n.successor().id):
            n.finger[1] = x
        n.successor().notify(n)

    ## ノードnnはPredecessorの可能性を考える
    def notify(n, nn):
        if n.predecessor == None or member_ll(nn.id, n.predecessor.id, n.id):
            n.predecessor = nn

    ## FingerTableエントリーを定期的に更新する
    def fix_fingers(n):
        i = random.randint(2,m) # ranfom index 2-160
        n.finger[i] = n.find_successor(n.start[i])



    def info_node(self):
        print "------------------------------------------------------------"
        print "IP:%4d, id: %s" % (self.ip, hex(self.id))
        print "   successor:%4d, predecessor:%4d" % (self.successor().ip, self.predecessor.ip)

    def info_connection(self):
        print "%4d -> [%4d] -> %4d" % (self.predecessor.ip, self.ip, self.successor().ip)

    def info_finger_table(self):
        print "finger table:"
        for k in range(1,m+1):
            print "k", k, "node:", self.finger[k].ip, "start:", hex(self.start[k])


    def check_successor(self, MAXSTACK=10000):
        print "+------------------------------------------------"
        print "| Check Successor  (from IP:", self.ip, ")"

        repeat_num = 0
        own  = self;
        next = self.successor()

        while True:
            print "|     %d -> %d" % (own.ip, next.ip)
            own = next;
            next = next.successor()
            repeat_num = repeat_num + 1
            if self.id == own.id:
                print "| Successor OK!"
                print "|     There are %d nodes in Chord Network" % (repeat_num)
                return repeat_num
            if own.id == next.id:
                print "| Error"
                print "|     Succesor is infinite looping  %d -> %d" % (own.ip, own.ip)
                return -1
            if MAXSTACK == repeat_num:
                print "| Stack OverFlow (repeat_num:%d)" % (repeat_num)
                print "|     1. There are more %d nodes in Chord Network" % (repeat_num)
                print "|     2. Chord Network is not completed or is broken"
                return -1

    def check_predecessor(self, MAXSTACK=10000):
        print "+------------------------------------------------"
        print "| Check Predecessor  (from IP:", self.ip, ")"

        repeat_num = 0
        own  = self;
        next = self.predecessor

        while True:
            print "|     %d <- %d" % (own.ip, next.ip)
            own = next;
            next = next.predecessor
            repeat_num = repeat_num + 1
            if self.id == own.id:
                print "| Predecessor OK!"
                print "|     There are %d nodes in Chord Network" % (repeat_num)
                return repeat_num
            if own.id == next.id:
                print "| Error"
                print "|     Predecessor is infinite looping  %d -> %d" % (own.ip, own.ip)
                return -1
            if MAXSTACK == repeat_num:
                print "| Stack OverFlow (repeat_num:%d)" % (repeat_num)
                print "|     1. There are more %d nodes in Chord Network" % (repeat_num)
                print "|     2. Chord Network is not completed or is broken"
                return -1
