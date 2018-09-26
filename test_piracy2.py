from jericho import *

walkthrough = 'x vent/get strip/open panel/touch wires with strip/get battery/open vent/s/s/e/kick vent/kick vent/kick vent/e/examine body/get pistol/get old battery/put new battery in gun/shoot door/n/e/s/move body/n/e/get datacube/s/d3179/confirm separation/n/w/n/u/w/get cutters/e/e/open lockers/search lockers/get all/w/d/e/e/e/touch pad/e/n/torch pipe/s/w/w/w/w/w/w/w/touch pad/w/n/cut cable with cutters/s/e/e/e/e/n/push button/n/n/n/push button/n/d/push m/u/e/put white datacube in slot/c4/c6/c7/get white datacube/put purple datacube in slot/c5/get purple datacube/c1/w/w/navcon, xcoord is 234 (Actual number will vary)/navcon, ycoord is 129 (Actual number will vary)/navcon, zcoord is 154 (Actual number will vary)/navcon, confirm course/e/d3180/confirm separation/shoot ceres/z/z/z/z/z/z/z/z/z/s/push button'

solution = walkthrough.split('/')

ROM_PATH="/home/matthew/workspace/TextWorld-baselines/games/piracy2.z5"

def test_piracy2():
    env = FrotzEnv(ROM_PATH, seed=4)
    env.reset()
    for act in solution:
        print(act, env.step(act))

def find_moves():
    env = FrotzEnv(ROM_PATH, seed=4)
    env.reset()
    old_ram = env.get_ram()
    d = {}
    cnt = 0
    for act in solution:
        cnt += 1
        obs, _, _, _ = env.step(act)
        print(obs)
        curr_ram = env.get_ram()
        diff = np.nonzero(old_ram - curr_ram)[0]
        for j in diff:
            if not j in d:
                d[j] = 1
            else:
                d[j] += 1
        old_ram = curr_ram
    s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    for key, value in s:
        print("{}: {}".format(key, value/float(cnt)))

def viz_objs():
    import pydot
    env = FrotzEnv(ROM_PATH, seed=5)
    print(env.reset())
    obs, score, done, _ = env.step('look')
    # world_objs = [env.get_object(i) for i in range(175)]
    world_objs = env.get_world_objects()
    for idx, o in enumerate(world_objs):
        print(idx, o)
    graph = pydot.Dot(graph_type='digraph')
    node2graph = {}
    for o in world_objs:
        if o and o.num > 0:
            graph_node = pydot.Node("{} {}\np{} s{} c{}".format(o.num, o.name, o.parent, o.sibling, o.child))
            if o.child <= 0:
                graph_node.add_style("filled")
            graph.add_node(graph_node)
            node2graph[o.num] = graph_node
    for o in world_objs:
        if o and o.num > 0:
            graph_node = node2graph[o.num]
            if o.sibling in node2graph:
                graph_sibling = node2graph[o.sibling]
                graph.add_edge(pydot.Edge(graph_node, graph_sibling, arrowhead='diamond'))
            if o.child in node2graph:
                child = node2graph[o.child]
                graph.add_edge(pydot.Edge(graph_node, child, color='blue'))
    graph.write_pdf('graph.pdf')

test_piracy2()
#find_moves()
#viz_objs()
