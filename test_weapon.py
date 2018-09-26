from jericho import *

walkthrough = "X room/Reply/X floor/X wall/X window/Reply/X Cheryl/X forms/X cheryl's key/X hologram/I/X pistol/fondle notch/read screen/x icons/x studs/x information stud/x powerup stud/touch it/x project status stud/touch generator/reply/x white pillar/reply/x panel/reply/reply/reply/open panel/touch panel/reply/x bay/x contact points/touch plasma generator/touch plasma containment/x generator/touch tool stud/reply/x probe/x sensors/top/bottom/take probe/touch top/point probe at points/press top/press bottom/z/sing/reply/look/x slot/take probe/probe contacts/touch bottom sensor/x hologram/point probe at slot/press top/z/point probe at contacts/press bottom/take probe/z/ask cheryl for hologram/wear goggles/x contacts/x generator/x bay/touch top/probe contacts/x studs/touch calibration/answer/probe ninth contact/points/take probe/point probe at calibration/probe contacts/touch calibration/put probe in contacts/press bottom/z/touch calibration/press powerup stud/take probe/shut panel/press powerup/reply/x project status stud/press project status stud/remove goggles/x status/x indicator/push generator access stud/press project status stud/put on goggles/x surface/give goggles to cheryl/touch sequence stud/g/give goggles to cheryl/press top/z/z/ask cheryl for goggles/press bottom/give goggles to cheryl/press sequence stud/x viewscreen/press sequence stud/x studs/x control/x transmit/x control stud/touch tool sutd/put probe in slab/touch bottom/touch tool stud/touch transmit stud/touch control stud/reply/z/cheryl, pull rods/take key/unlock handcuffs with key/remove handcuffs/pull rods/put handcuffs on rods/reply/press information/press forcefield/touch ignition/reply/reply/reply/g/g/reply/reply/reply/reply/laugh/wave/z/push ignition"

solution = walkthrough.split('/')

ROM_PATH="/home/matthew/workspace/TextWorld-baselines/games/weapon.z5"

def print_object_tree(root_obj, world_objs, indent=''):
    for obj in world_objs:
        if obj.parent == root_obj.num:
            print("{}{}".format(indent, obj))
            if obj.child != 0:
                print_object_tree(obj, world_objs, indent+'  ')


def test_weapon():
    env = FrotzEnv(ROM_PATH, seed=4)
    env.reset()
    for act in solution:
        print("{} {}".format(act, env.step(act)))
        loc = env.get_player_location()
        print("Loc {}-{}".format(loc.name, loc.num))
        for i in env.get_inventory():
            print("  {}-{}".format(i.name, i.num))
        print_object_tree(loc, env.get_world_objects())
        print(env.get_world_diff())
        print('')

def test_max_score():
    env = FrotzEnv(ROM_PATH, seed=4)
    assert env.get_max_score() == 1

# def test_load_save_file():
#     fname = 'weapon.qzl'
#     env = FrotzEnv(ROM_PATH, seed=4)
#     env.reset()
#     soln_size = len(solution)
#     for act in solution[:int(soln_size/2)]:
#         orig_obs, _, _, _ = env.step(act)
#     if os.path.exists(fname):
#         os.remove(fname)
#     env.save(fname)
#     orig_obs, _, _, _ = env.step('look')
#     for act in solution[int(soln_size/2):soln_size]:
#         new_obs, _, _, _ = env.step(act)
#     assert new_obs != orig_obs
#     env.load(fname)
#     restored, _, _, _ = env.step('look')
#     assert restored == orig_obs
#     if os.path.exists(fname):
#         os.remove(fname)

# def test_load_save_str():
#     env = FrotzEnv(ROM_PATH, seed=4)
#     env.reset()
#     soln_size = len(solution)
#     for act in solution[:int(soln_size/2)]:
#         orig_obs, _, _, _ = env.step(act)
#     save = env.save_str()
#     orig_obs, _, _, _ = env.step('look')
#     for act in solution[int(soln_size/2):soln_size]:
#         new_obs, _, _, _ = env.step(act)
#     assert new_obs != orig_obs
#     env.load_str(save)
#     restored, _, _, _ = env.step('look')
#     assert restored == orig_obs, "Orig: {}, Restored {}".format(orig_obs, restored)

def manual_score(env, obs):
    obs, _, _, _ = env.step('score')
    print(obs)
    pattern = 'You have so far scored '
    start = obs.index(pattern)
    end = obs.index(' out of a possible')
    score = int(obs[start+len(pattern):end])
    return score

# def manual_score(env, obs):
#     idx = obs.rfind(':')
#     return -int(obs[idx+1:])

# def manual_moves(env, obs):
#     idx = obs.index('/')
#     return int(obs[idx+1:obs.index('\n',idx)])

def test_score_detection():
    env = FrotzEnv(ROM_PATH, seed=5)
    env.reset()
    for act in solution:
        obs, score, done, _ = env.step(act)
        assert manual_score(env, obs) == score

# def test_move_detection():
#     env = FrotzEnv(ROM_PATH, seed=5)
#     env.reset()
#     for idx, act in enumerate(solution[:30]):
#         obs, score, done, info = env.step(act)
#         assert info['moves'] == manual_moves(env, obs)

def test_inventory():
    env = FrotzEnv(ROM_PATH, seed=5)
    env.reset()
    # for act in solution:
    #     env.step(act)
    inv = env.get_inventory()
    inv_names = [o.name for o in inv]
    assert 'Steel key' in inv_names


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

# def find_moves():
#     env = FrotzEnv(ROM_PATH, seed=5)
#     env.reset()
#     old_ram = env.get_ram()
#     d = {}
#     cnt = 0
#     for act in solution:
#         cnt += 1
#         obs, _, _, _ = env.step(act)
#         moves = manual_moves(env, obs)
#         curr_ram = env.get_ram()
#         for idx, v in enumerate(curr_ram):
#             if v == moves:
#                 if not idx in d:
#                     d[idx] = 1
#                 else:
#                     d[idx] += 1
#         old_ram = curr_ram
#     s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
#     for key, value in s:
#         if value/float(cnt) > .9:
#             print("{}: {}".format(key, value/float(cnt)))

# def test_world_change():
#     env = FrotzEnv(ROM_PATH, seed=5)
#     env.reset()
#     for act in solution:
#         obs, _, _, _ = env.step(act)
#         assert env.world_changed(),\
#             "Expected world change: Act: \"{}\" Obs: \"{}\" Diff: {}"\
#             .format(act, obs, env.get_world_diff())

# def test_game_over():
#     env = FrotzEnv(ROM_PATH, seed=4)
#     env.reset()
#     for act in solution:
#         env.step(act)
#         assert not env.game_over()

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

test_weapon()
# find_moves()
# find_score()
# viz_objs()
