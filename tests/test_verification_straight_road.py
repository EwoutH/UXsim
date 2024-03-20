"""
This script verifies whether UXsim outputs reasonable solutions for a straight road in various configurations.
"""

import pytest
from uxsim import *

def equal_tolerance(val, check, rel_tol=0.1, abs_tol=0.0):
    if check == 0:
        abs_tol = 0.1
    return abs(val - check) <= abs(check*rel_tol) + abs_tol

"""
default FD:
    u = 20
    kappa = 0.2
    tau = 1
    w = 5
    k^* = 0.04
    q^* = 0.8
"""

def test_1link():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("dest", 1, 1)
    link = W.addLink("link", "orig", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.5)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 250)
    assert equal_tolerance(W.analyzer.trip_completed, 250)
    assert equal_tolerance(W.analyzer.total_travel_time, 12500)
    assert equal_tolerance(W.analyzer.average_travel_time, 50)
    assert equal_tolerance(W.analyzer.average_delay, 0)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link.q_mat[2, 5], 0.5)
    assert equal_tolerance(link.q_mat[7, 5], 0)
    assert equal_tolerance(link.k_mat[2, 5], 0.025)
    assert equal_tolerance(link.k_mat[7, 5], 0)
    assert equal_tolerance(link.v_mat[2, 5], 20)
    assert equal_tolerance(link.v_mat[7, 5], 20)

def test_1link_deltan1():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("dest", 1, 1)
    link = W.addLink("link", "orig", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.5)

    W.exec_simulation()

    W.analyzer.print_simple_stats()


    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 250)
    assert equal_tolerance(W.analyzer.trip_completed, 250)
    assert equal_tolerance(W.analyzer.total_travel_time, 12500)
    assert equal_tolerance(W.analyzer.average_travel_time, 50)
    assert equal_tolerance(W.analyzer.average_delay, 0)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link.q_mat[2, 5], 0.5)
    assert equal_tolerance(link.q_mat[7, 5], 0)
    assert equal_tolerance(link.k_mat[2, 5], 0.025)
    assert equal_tolerance(link.k_mat[7, 5], 0)
    assert equal_tolerance(link.v_mat[2, 5], 20)
    assert equal_tolerance(link.v_mat[7, 5], 20)

def test_1link_maxflow():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("dest", 1, 1)
    link = W.addLink("link", "orig", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 2000, 2)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link.q_mat[2, 5], 0.8)
    assert equal_tolerance(link.q_mat[7, 5], 0.8)
    assert equal_tolerance(link.k_mat[2, 5], 0.04)
    assert equal_tolerance(link.k_mat[7, 5], 0.04)
    assert equal_tolerance(link.v_mat[2, 5], 20)
    assert equal_tolerance(link.v_mat[7, 5], 20)    

def test_1link_maxflow_deltan1():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("dest", 1, 1)
    link = W.addLink("link", "orig", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 2000, 2)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link.q_mat[2, 5], 0.8)
    assert equal_tolerance(link.q_mat[7, 5], 0.8)
    assert equal_tolerance(link.k_mat[2, 5], 0.04)
    assert equal_tolerance(link.k_mat[7, 5], 0.04)
    assert equal_tolerance(link.v_mat[2, 5], 20)
    assert equal_tolerance(link.v_mat[7, 5], 20) 

def test_2link():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=10, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.5)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 250)
    assert equal_tolerance(W.analyzer.trip_completed, 250)
    assert equal_tolerance(W.analyzer.total_travel_time, 37500)
    assert equal_tolerance(W.analyzer.average_travel_time, 150)
    assert equal_tolerance(W.analyzer.average_delay, 0)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.5)
    assert equal_tolerance(link1.q_mat[7, 5], 0)
    assert equal_tolerance(link1.k_mat[2, 5], 0.025)
    assert equal_tolerance(link1.k_mat[7, 5], 0)
    assert equal_tolerance(link1.v_mat[2, 5], 20)
    assert equal_tolerance(link1.v_mat[7, 5], 20)
    assert equal_tolerance(link2.q_mat[2, 5], 0.5)
    assert equal_tolerance(link2.q_mat[7, 5], 0)
    assert equal_tolerance(link2.k_mat[2, 5], 0.05)
    assert equal_tolerance(link2.k_mat[7, 5], 0)
    assert equal_tolerance(link2.v_mat[2, 5], 10)
    assert equal_tolerance(link2.v_mat[7, 5], 10)

def test_2link_deltan1():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=10, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.5)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 250)
    assert equal_tolerance(W.analyzer.trip_completed, 250)
    assert equal_tolerance(W.analyzer.total_travel_time, 37500)
    assert equal_tolerance(W.analyzer.average_travel_time, 150)
    assert equal_tolerance(W.analyzer.average_delay, 0)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.5)
    assert equal_tolerance(link1.q_mat[7, 5], 0)
    assert equal_tolerance(link1.k_mat[2, 5], 0.025)
    assert equal_tolerance(link1.k_mat[7, 5], 0)
    assert equal_tolerance(link1.v_mat[2, 5], 20)
    assert equal_tolerance(link1.v_mat[7, 5], 20)
    assert equal_tolerance(link2.q_mat[2, 5], 0.5)
    assert equal_tolerance(link2.q_mat[7, 5], 0)
    assert equal_tolerance(link2.k_mat[2, 5], 0.05)
    assert equal_tolerance(link2.k_mat[7, 5], 0)
    assert equal_tolerance(link2.v_mat[2, 5], 10)
    assert equal_tolerance(link2.v_mat[7, 5], 10)

def test_2link_maxflow():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 2000, 2)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.8)
    assert equal_tolerance(link1.q_mat[7, 5], 0.8)
    assert equal_tolerance(link1.k_mat[2, 5], 0.04)
    assert equal_tolerance(link1.k_mat[7, 5], 0.04)
    assert equal_tolerance(link1.v_mat[2, 5], 20)
    assert equal_tolerance(link1.v_mat[7, 5], 20)
    assert equal_tolerance(link2.q_mat[2, 5], 0.8)
    assert equal_tolerance(link2.q_mat[7, 5], 0.8)
    assert equal_tolerance(link2.k_mat[2, 5], 0.04)
    assert equal_tolerance(link2.k_mat[7, 5], 0.04)
    assert equal_tolerance(link2.v_mat[2, 5], 20)
    assert equal_tolerance(link2.v_mat[7, 5], 20)

def test_2link_maxflow_deltan1():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 2000, 2)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.8)
    assert equal_tolerance(link1.q_mat[7, 5], 0.8)
    assert equal_tolerance(link1.k_mat[2, 5], 0.04)
    assert equal_tolerance(link1.k_mat[7, 5], 0.04)
    assert equal_tolerance(link1.v_mat[2, 5], 20)
    assert equal_tolerance(link1.v_mat[7, 5], 20)
    assert equal_tolerance(link2.q_mat[2, 5], 0.8)
    assert equal_tolerance(link2.q_mat[7, 5], 0.8)
    assert equal_tolerance(link2.k_mat[2, 5], 0.04)
    assert equal_tolerance(link2.k_mat[7, 5], 0.04)
    assert equal_tolerance(link2.v_mat[2, 5], 20)
    assert equal_tolerance(link2.v_mat[7, 5], 20)

def test_2link_bottleneck_due_to_free_flow_speed():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=10, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.8)
    W.adddemand("orig", "dest", 500, 1500, 0.4)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 800)
    assert equal_tolerance(W.analyzer.trip_completed, 800)
    assert equal_tolerance(W.analyzer.total_travel_time, 146000.0)
    assert equal_tolerance(W.analyzer.average_travel_time, 182.5)
    assert equal_tolerance(W.analyzer.average_delay, 32.5)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.06667) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 10) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.4) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.02) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.6667) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.06667) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 10) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.4) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.04) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 10) #freeflow

def test_2link_bottleneck_due_to_free_flow_speed_deltan1():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=10, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.8)
    W.adddemand("orig", "dest", 500, 1500, 0.4)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 800)
    assert equal_tolerance(W.analyzer.trip_completed, 800)
    assert equal_tolerance(W.analyzer.total_travel_time, 146000.0)
    assert equal_tolerance(W.analyzer.average_travel_time, 182.5)
    assert equal_tolerance(W.analyzer.average_delay, 32.5)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.06667) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 10) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.4) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.02) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.6667) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.06667) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 10) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.4) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.04) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 10) #freeflow

def test_2link_bottleneck_due_to_capacity_out():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2, capacity_out=0.66666)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.8)
    W.adddemand("orig", "dest", 500, 1500, 0.4)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 800)
    assert equal_tolerance(W.analyzer.trip_completed, 800)
    assert equal_tolerance(W.analyzer.total_travel_time, 104775)
    assert equal_tolerance(W.analyzer.average_travel_time, 131)
    assert equal_tolerance(W.analyzer.average_delay, 31)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.06667) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 10) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.4) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.02) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.6667) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.03333) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 20) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.4) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.02) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 20) #freeflow

def test_2link_bottleneck_due_to_capacity_out_deltan1():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2, capacity_out=0.66666)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.8)
    W.adddemand("orig", "dest", 500, 1500, 0.4)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 800)
    assert equal_tolerance(W.analyzer.trip_completed, 800)
    assert equal_tolerance(W.analyzer.total_travel_time, 104775)
    assert equal_tolerance(W.analyzer.average_travel_time, 131)
    assert equal_tolerance(W.analyzer.average_delay, 31)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.06667) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 10) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.4) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.02) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.6667) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.03333) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 20) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.4) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.02) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 20) #freeflow

def test_2link_bottleneck_due_to_jam_density():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.1)
    W.adddemand("orig", "dest", 0, 500, 0.8)
    W.adddemand("orig", "dest", 500, 1500, 0.4)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 800)
    assert equal_tolerance(W.analyzer.trip_completed, 800)
    assert equal_tolerance(W.analyzer.total_travel_time, 106000)
    assert equal_tolerance(W.analyzer.average_travel_time, 132.5)
    assert equal_tolerance(W.analyzer.average_delay, 32.5)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.06667) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 10) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.4) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.02) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.6667) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.03333) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 20) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.4) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.02) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 20) #freeflow

def test_2link_bottleneck_due_to_node_capacity():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1, flow_capacity=0.666)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.8)
    W.adddemand("orig", "dest", 500, 1500, 0.4)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 800)
    assert equal_tolerance(W.analyzer.trip_completed, 800)
    assert equal_tolerance(W.analyzer.total_travel_time, 106000)
    assert equal_tolerance(W.analyzer.average_travel_time, 132.5)
    assert equal_tolerance(W.analyzer.average_delay, 32.5)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.06667) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 10) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.4) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.02) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.6667) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.03333) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 20) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.4) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.02) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 20) #freeflow

def test_2link_bottleneck_due_to_node_capacity_deltan1():
    W = World(
        name="",
        deltan=1, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1, flow_capacity=0.666)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 0, 500, 0.8)
    W.adddemand("orig", "dest", 500, 1500, 0.4)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 800)
    assert equal_tolerance(W.analyzer.trip_completed, 800)
    assert equal_tolerance(W.analyzer.total_travel_time, 106000)
    assert equal_tolerance(W.analyzer.average_travel_time, 132.5)
    assert equal_tolerance(W.analyzer.average_delay, 32.5)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.06667) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 10) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.4) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.02) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.6667) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.03333) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 20) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.4) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.02) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 20) #freeflow

def test_2link_leave_at_middle():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1)
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "mid", 0, 500, 0.666)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 330)
    assert equal_tolerance(W.analyzer.trip_completed, 330)
    assert equal_tolerance(W.analyzer.total_travel_time, 17300)
    assert equal_tolerance(W.analyzer.average_travel_time, 52.4)
    assert equal_tolerance(W.analyzer.average_delay, 2.4)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[2, 5], 0.6667) #congestion before BN
    assert equal_tolerance(link1.k_mat[2, 5], 0.03333) #congestion before BN
    assert equal_tolerance(link1.v_mat[2, 5], 20) #congestion before BN
    assert equal_tolerance(link1.q_mat[7, 5], 0.0) #freeflow
    assert equal_tolerance(link1.k_mat[7, 5], 0.0) #freeflow
    assert equal_tolerance(link1.v_mat[7, 5], 20) #freeflow
    assert equal_tolerance(link2.q_mat[2, 5], 0.0) #freeflow after BN
    assert equal_tolerance(link2.k_mat[2, 5], 0.0) #freeflow after BN
    assert equal_tolerance(link2.v_mat[2, 5], 20) #freeflow after BN
    assert equal_tolerance(link2.q_mat[8, 5], 0.0) #freeflow
    assert equal_tolerance(link2.k_mat[8, 5], 0.0) #freeflow 
    assert equal_tolerance(link2.v_mat[8, 5], 20) #freeflow

def test_3link_queuespillback():

    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid1", 1, 1)
    W.addNode("mid2", 2, 2)
    W.addNode("dest", 3, 3)
    link1 = W.addLink("link", "orig", "mid1", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid1", "mid2", length=1000, free_flow_speed=20, jam_density=0.2, capacity_out=0.4)
    link3 = W.addLink("link", "mid2", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    t1 = 400
    t2 = 800
    W.adddemand("orig", "dest", 0, t1, 0.8)
    W.adddemand("orig", "dest", t1, t2, 0.4)
    W.adddemand("orig", "dest", t2, 2000, 0.1)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()

    assert equal_tolerance(W.analyzer.trip_all, 600)
    assert equal_tolerance(W.analyzer.trip_completed, 585)
    assert equal_tolerance(W.analyzer.total_travel_time, 221050)
    assert equal_tolerance(W.analyzer.average_travel_time, 378)
    assert equal_tolerance(W.analyzer.average_delay, 228)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[1, 8], 0.8, rel_tol=0.2) #before congestion
    assert equal_tolerance(link1.k_mat[1, 8], 0.04, rel_tol=0.2) #before congestion
    assert equal_tolerance(link1.v_mat[1, 8], 20, rel_tol=0.2) #before congestion
    assert equal_tolerance(link1.q_mat[5, 8], 0.4, rel_tol=0.2) #during congestion
    assert equal_tolerance(link1.k_mat[5, 8], 0.12, rel_tol=0.2) #during congestion
    assert equal_tolerance(link1.v_mat[5, 8], 3.33, rel_tol=0.2) #during congestion
    assert equal_tolerance(link1.q_mat[10, 8], 0.08, rel_tol=0.2) #after congestion
    assert equal_tolerance(link1.k_mat[10, 8], 0.004, rel_tol=0.2) #after congestion
    assert equal_tolerance(link1.v_mat[10, 8], 20, rel_tol=0.2) #after congestion

    assert equal_tolerance(link2.q_mat[5, 8], 0.4, rel_tol=0.2) #during congestion
    assert equal_tolerance(link2.k_mat[5, 8], 0.12, rel_tol=0.2) #during congestion
    assert equal_tolerance(link2.v_mat[5, 8], 3.33, rel_tol=0.2) #during congestion
    assert equal_tolerance(link2.q_mat[13, 8], 0.08, rel_tol=0.2) #after congestion
    assert equal_tolerance(link2.k_mat[13, 8], 0.004, rel_tol=0.2) #after congestion 
    assert equal_tolerance(link2.v_mat[13, 8], 20, rel_tol=0.2) #after congestion

    assert equal_tolerance(link3.q_mat[5, 8], 0.4, rel_tol=0.2) #during congestion
    assert equal_tolerance(link3.k_mat[5, 8], 0.02, rel_tol=0.2) #during congestion
    assert equal_tolerance(link3.v_mat[5, 8], 20, rel_tol=0.2) #during congestion
    assert equal_tolerance(link3.q_mat[15, 8], 0.08, rel_tol=0.2) #after congestion
    assert equal_tolerance(link3.k_mat[15, 8], 0.004, rel_tol=0.2) #after congestion 
    assert equal_tolerance(link3.v_mat[15, 8], 20, rel_tol=0.2) #after congestion

def test_2link_signal():
    W = World(
        name="",
        deltan=5, 
        tmax=2000, 
        print_mode=1, save_mode=1, show_mode=1,
        random_seed=0
    )

    W.addNode("orig", 0, 0)
    W.addNode("mid", 1, 1, signal=[60,60])
    W.addNode("dest", 2, 2)
    link1 = W.addLink("link", "orig", "mid", length=1000, free_flow_speed=20, jam_density=0.2)
    link2 = W.addLink("link", "mid", "dest", length=1000, free_flow_speed=20, jam_density=0.2)
    W.adddemand("orig", "dest", 300, 800, 0.4)
    W.adddemand("orig", "dest", 0, 2000, 0.2)

    W.exec_simulation()

    W.analyzer.print_simple_stats()

    W.analyzer.basic_analysis()
    assert equal_tolerance(W.analyzer.trip_all, 600)
    assert equal_tolerance(W.analyzer.trip_completed, 570)
    assert equal_tolerance(W.analyzer.total_travel_time, 107100)
    assert equal_tolerance(W.analyzer.average_travel_time, 188)
    assert equal_tolerance(W.analyzer.average_delay, 88)

    W.analyzer.compute_edie_state()
    assert equal_tolerance(link1.q_mat[:,8].mean() , 0.29947916666666663)
    assert equal_tolerance(link1.k_mat[:,8].mean() , 0.054958767361111105)
    assert equal_tolerance(link1.v_mat[:,8].mean() , 12.86046633191759)
    assert equal_tolerance(link1.q_mat[:,2].mean() , 0.3020833333333333)
    assert equal_tolerance(link1.k_mat[:,2].mean() , 0.026356336805555557)
    assert equal_tolerance(link1.v_mat[:,2].mean() , 17.49905597926791)
    assert equal_tolerance(link1.q_mat[8,:].mean() , 0.309375)
    assert equal_tolerance(link1.k_mat[8,:].mean() , 0.06661458333333334)
    assert equal_tolerance(link1.v_mat[8,:].mean() , 9.633282431298722)
    assert equal_tolerance(link1.q_mat[12,:].mean(),  0.19687499999999997)
    assert equal_tolerance(link1.k_mat[12,:].mean(),  0.011875)
    assert equal_tolerance(link1.v_mat[12,:].mean(),  18.607142857142858)
    assert equal_tolerance(link2.q_mat[:,8].mean() , 0.29427083333333337)
    assert equal_tolerance(link2.k_mat[:,8].mean() , 0.014713541666666666)
    assert equal_tolerance(link2.v_mat[:,8].mean() , 20.0)


