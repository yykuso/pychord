# -*- coding: utf-8 -*-
from chord import *
# from time import sleep

network = Network()
for i in range(100):
    # network.single_join(i)
    network.multi_join(i)
network.info()
network.time_elapsed(10)
network.check_ring()
network.time_elapsed(100000)
network.check_ring()


# # 抜けたときの挙動
# print network.join_list
# del network.join_list[5]
# print network.join_list
#
# network.time_elapsed(100)
