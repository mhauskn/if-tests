from jericho import *

walkthrough = 'stand up/i/x smelling salts/read tag/x note/l/l/l/x door/open door/l/l/l/scream/e/x falcon/read missive/falcon, yes/x davis/x ring/x falcon/z/z/stand up/look around/look through window/open curtain/x cupboard/x table/x bed/z/x brooch/open coffer/take invitation/read invitation/n/d/n/x gate/n/take bottle/take mirror/x bottle/read label/s/s/u/open door/enter/take clothes/remove dress/wear breeches/wear shirt/z/out/s/take coffer/z/throw coffer through window/sit on ledge/put all in reticule/take ladder'
solution = walkthrough.split('/')

def test_plundered():
    env = FrotzEnv("../../TextWorld-baselines/games/plundered.z3", seed=6)
    env.reset()
    for act in solution:
        print("{} {}".format(act, env.step(act)))
        loc = env.get_player_location()
        print("Loc {}-{}".format(loc.name, loc.num))
        for i in env.get_inventory():
            print("  {}-{}".format(i.name, i.num))
        print('')

def test_max_score():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    assert env.get_max_score() == 25

def test_load_save_file():
    fname = 'plundered.qzl'
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    for act in solution[:15]:
        orig_obs, _, _, _ = env.step(act)
    if os.path.exists(fname):
        os.remove(fname)
    env.save(fname)
    orig_obs, _, _, _ = env.step('look')
    orig_obs = orig_obs[orig_obs.index('The room'):]
    for act in solution[15:]:
        new_obs, _, _, _ = env.step(act)
    assert new_obs != orig_obs
    env.load(fname)
    restored, _, _, _ = env.step('look')
    restored = restored[restored.index('The room'):]
    assert restored == orig_obs
    if os.path.exists(fname):
        os.remove(fname)

def test_load_save_str():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    for act in solution[:15]:
        orig_obs, _, _, _ = env.step(act)
    save = env.save_str()
    orig_obs, _, _, _ = env.step('look')
    orig_obs = orig_obs[orig_obs.index('The room'):]
    for act in solution[15:]:
        new_obs, _, _, _ = env.step(act)
    assert new_obs != orig_obs
    env.load_str(save)
    restored, _, _, _ = env.step('look')
    restored = restored[restored.index('The room'):]
    assert restored == orig_obs, "Orig: {}, Restored {}".format(orig_obs, restored)

def manual_score(env, obs):
    a = 'Score: '
    print(obs)
    idx = obs.index(a)
    return int(obs[idx+len(a):obs.index(' Moves:',idx)])

def manual_moves(env, obs):
    a = 'Moves: '
    idx = obs.index(a)
    return int(obs[idx+len(a):obs.index('\n',idx)])

def test_score_detection():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    env.step(solution[0])
    old_score = 0
    for act in solution[1:14]:
        obs, score, done, _ = env.step(act)
        assert manual_score(env, obs) == old_score
        old_score = score

def test_move_detection():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    env.step(solution[0])
    for idx, act in enumerate(solution[1:14]):
        obs, score, done, info = env.step(act)
        assert info['moves'] == manual_moves(env, obs) + 1

def test_inventory():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    for act in solution:
        env.step(act)
    inv = env.get_inventory()
    inv_names = [o.name for o in inv]
    assert 'shirt' in inv_names

def find_score():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    old_ram = env.get_ram()
    d = {}
    cnt = 0
    env.step(solution[0])
    for act in solution[1:]:
        cnt += 1
        obs, _, _, _ = env.step(act)
        if 'TWO DAYS LATER' in obs:
            continue
        score = manual_score(env, obs)
        print(obs, score)
        curr_ram = env.get_ram()
        for idx, v in enumerate(curr_ram):
            if v == score:
                if not idx in d:
                    d[idx] = 1
                else:
                    d[idx] += 1
        old_ram = curr_ram
    s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    for key, value in s:
        if value/float(cnt) > .9:
            print("{}: {}".format(key, value/float(cnt)))

def find_moves():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    old_ram = env.get_ram()
    d = {}
    cnt = 0
    env.step(solution[0])
    for act in solution[1:14]:
        cnt += 1
        obs, _, _, _ = env.step(act)
        print(obs)
        moves = manual_moves(env, obs)
        print('Moves',moves)
        curr_ram = env.get_ram()
        for idx, v in enumerate(curr_ram):
            if v == moves + 1:
                if not idx in d:
                    d[idx] = 1
                else:
                    d[idx] += 1
        old_ram = curr_ram
    s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    for key, value in s:
        if value/float(cnt) > .8:
            print("{}: {}".format(key, value/float(cnt)))

# def test_world_change():
#     env = FrotzEnv("../roms/plundered.z3", seed=6)
#     env.reset()
#     for act in solution:
#         obs, _, _, _ = env.step(act)
#         assert env.world_changed(),\
#             "Expected world change: Act: \"{}\" Obs: \"{}\" Diff: {}"\
#             .format(act, obs, env.get_world_diff())

def test_game_over():
    env = FrotzEnv("../roms/plundered.z3", seed=6)
    env.reset()
    for act in solution:
        env.step(act)
        assert not env.game_over()

def viz_objs():
    import pydot
    env = FrotzEnv("../roms/plundered.z3", seed=6)
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

test_plundered()
#find_moves()
#find_score()
#viz_objs()
