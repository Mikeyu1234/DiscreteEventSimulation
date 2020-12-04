import random
import functools

import simpy

import scipy.stats
import numpy as np

from SimComponents import PacketGenerator, PacketSink, SwitchPort, RandomBrancher,PortMonitor


if __name__ == '__main__':

    mean_pkt_size = 100.0
    adist =functools.partial(random.expovariate,0.5) #exploentioal arrival time
    sdist =functools.partial(random.expovariate, 0.01) #Mean size of packet 100 bytes
    #port_rate = float(functools.partial(random.expovariate,0.5)) # Servace Bit Rate
    port_rate = 1000.0
    samp_dist1 = functools.partial(random.expovariate, 1.0)
    samp_dist2 = functools.partial(random.expovariate, 1.0)
    qlimit = 10000 #FIFO Queue Size
    env = simpy.Environment()

    pg = PacketGenerator(env, "Greg", adist, sdist)#Package Generator
    ps1 = PacketSink(env, debug=False, rec_arrivals=True) #Package Sink for packages
    ps2 = PacketSink(env, debug=False, rec_arrivals=True)

    switch_port1 = SwitchPort(env, port_rate, qlimit=10000)# define two queues
    switch_port2 = SwitchPort(env, port_rate, qlimit=10000)

    pm1 = PortMonitor(env, switch_port1, samp_dist1)#define port monitor
    pm2 = PortMonitor(env, switch_port2, samp_dist2)

    pg.out = switch_port1
    '''switch_port1.out = ps1
    ps1 = switch_port2
    '''

    switch_port1.out = switch_port2
    switch_port2.out = ps2


    env.run(until=2000)
    #print(ps2.waits[-10:])
    print("average wait = {:.3f}".format(sum(ps2.waits)/len(ps2.waits)))

    #theorical Mean Sojourn Time
    

    #Calculate CI
    confidence_level = 0.95
    degrees_freedom = len(ps2.waits) - 1
    sample_mean = np.mean(ps2.waits)
    sample_standard_error = scipy.stats.sem(ps2.waits)
    confidence_interval = scipy.stats.t.interval(confidence_level, degrees_freedom, sample_mean, sample_standard_error)

    

    print("Wait Time CI =  {}".format(confidence_interval) )

    print("loss rate1: {}".format(float(switch_port1.packets_drop)/switch_port1.packets_rec))
    print("loss rate2: {}".format(float(switch_port2.packets_drop)/switch_port2.packets_rec))











    '''
    # Set up arrival and packet size distributions
    # Using Python functools to create callable functions for random variates with fixed parameters.
    # each call to these will produce a new random value.
    mean_pkt_size = 100.0  # in bytes
    adist1 = functools.partial(random.expovariate, 2.0)
    adist2 = functools.partial(random.expovariate, 0.5)
    #adist3 = functools.partial(random.expovariate, 0.6)
    sdist = functools.partial(random.expovariate, 1.0/mean_pkt_size)
    samp_dist = functools.partial(random.expovariate, 0.50)
    port_rate = functools.partial(random.expovariate, 2.0)  # exploential service time

    # Create the SimPy environment. This is the thing that runs the simulation.
    env = simpy.Environment()

    # Create the packet generators and sink
    def selector(pkt):
        return pkt.src == "SJSU1"

    def selector2(pkt):
        return pkt.src == "SJSU2"
    ps1 = PacketSink(env, debug=False, rec_arrivals=True)
    ps2 = PacketSink(env, debug=False, rec_arrivals=True)
    pg1 = PacketGenerator(env, "SJSU1", adist1, sdist)
    switch_port1 = SwitchPort(env, port_rate, qlimit=10000)
    switch_port2 = SwitchPort(env, port_rate, qlimit=10000)
    #switch_port3 = SwitchPort(env, port_rate)
    #switch_port4 = SwitchPort(env, port_rate)

    # Wire packet generators, switch ports, and sinks together
    pg1.out = switch_port1
    switch_port1.out = ps1
    switch_port1.out=switch_port2
    switch_port2.out = ps2
    

    
    # Run it
    env.run(until=4000)
    print(ps2.waits[-10:])
    # print pm.sizes[-10:]
    # print ps.arrivals[-10:]
    print("average wait source 1 to output 3 = {}".format(sum(ps1.waits)/len(ps1.waits)))
    print("average wait source 2 to output 4 = {}".format(sum(ps2.waits)/len(ps2.waits)))
    print("packets sent {}".format(pg1.packets_sent + pg2.packets_sent))
    print("packets received: {}".format(len(ps2.waits)))
    # print "average system occupancy: {}".format(float(sum(pm.sizes))/len(pm.sizes))

    '''