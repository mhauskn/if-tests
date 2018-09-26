from jericho import *

walkthrough = 'l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/l/open door4/look/l/l/l/l/east/l/open L-box/l/take key9 from L-box/put key9 on stand4'

solution = walkthrough.split('/')

def test_textworld():
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    env.reset()
    for act in solution:
        print(act, env.step(act),'\n')

def test_max_score():
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    assert env.get_max_score() == 100

def test_load_save_file():
    fname = 'textworld.qzl'
    description = 'This is'
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    env.reset()
    for act in solution[:10]:
        orig_obs, _, _, _ = env.step(act)
    if os.path.exists(fname):
        os.remove(fname)
    env.save(fname)
    orig_obs, _, _, _ = env.step('look')
    # orig_obs = orig_obs[orig_obs.index(description):]
    for act in solution[10:15]:
        new_obs, _, _, _ = env.step(act)
    assert new_obs != orig_obs
    env.load(fname)
    restored, _, _, _ = env.step('look')
    # restored = restored[restored.index(description):]
    assert restored == orig_obs
    if os.path.exists(fname):
        os.remove(fname)

def test_load_save_str():
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    description = 'A grim'
    env.reset()
    for act in solution[:10]:
        orig_obs, _, _, _ = env.step(act)
    save = env.save_str()
    orig_obs, _, _, _ = env.step('look')
    # orig_obs = orig_obs[orig_obs.index(description):]
    for act in solution[10:15]:
        new_obs, _, _, _ = env.step(act)
    assert new_obs != orig_obs
    env.load_str(save)
    restored, _, _, _ = env.step('look')
    # restored = restored[restored.index(description):]
    assert restored == orig_obs, "Orig: {}, Restored {}".format(orig_obs, restored)

def manual_score(env, obs):
    obs, _, _, _ = env.step('score')
    print(obs)
    pattern = 'You have so far scored '
    start = obs.index(pattern)
    end = obs.index(' out of a possible')
    score = int(obs[start+len(pattern):end])
    return score

def manual_moves(env, obs):
    obs, _, _, _ = env.step('score')
    print(obs)
    a = ', in '
    idx = obs.index(a)
    return int(obs[idx+len(a):obs.index(' turn',idx)])

# def manual_score(env, obs):
#     a = 'Score: '
#     print(obs)
#     idx = obs.index(a)
#     return int(obs[idx+len(a):obs.index(' Moves:',idx)])

# def manual_moves(env, obs):
#     a = 'Moves: '
#     idx = obs.index(a)
#     return int(obs[idx+len(a):obs.index('\n',idx)])

def test_score_detection():
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    env.reset()
    for act in solution:
        obs, score, done, _ = env.step(act)
        assert manual_score(env, obs) == score

# def test_move_detection():
#     env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
#     env.reset()
#     for idx, act in enumerate(solution):
#         obs, score, done, info = env.step(act)
#         assert info['moves'] == idx + 2

def test_inventory():
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    env.reset()
    for act in solution:
        env.step(act)
    inv = env.get_inventory()
    inv_names = [o.name for o in inv]
    assert 'flashlight' in inv_names

def find_score():
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    env.reset()
    old_ram = env.get_ram()
    d = {}
    cnt = 0
    for act in solution:
        cnt += 1
        obs, _, _, _ = env.step(act)
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
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    env.reset()
    old_ram = env.get_ram()
    d = {}
    cnt = 0
    for act in solution[:-1]:
        cnt += 1
        obs, _, _, _ = env.step(act)
        print(obs)
        moves = manual_moves(env, obs)
        print('Moves',moves)
        curr_ram = env.get_ram()
        for idx, v in enumerate(curr_ram):
            if v == moves:
                if not idx in d:
                    d[idx] = 1
                else:
                    d[idx] += 1
        old_ram = curr_ram
    s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
    for key, value in s:
        if value/float(cnt) > .8:
            print("{}: {}".format(key, value/float(cnt)))

# def find_moves():
#     env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=4)
#     env.reset()
#     old_ram = env.get_ram()
#     d = {}
#     cnt = 0
#     for act in solution:
#         cnt += 1
#         obs, _, _, _ = env.step(act)
#         print(obs)
#         curr_ram = env.get_ram()
#         diff = np.nonzero(old_ram - curr_ram)[0]
#         for j in diff:
#             if not j in d:
#                 d[j] = 1
#             else:
#                 d[j] += 1
#         old_ram = curr_ram
#     s = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
#     for key, value in s:
#         print("{}: {}".format(key, value/float(cnt)))

def test_game_over():
    env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    env.reset()
    for act in solution:
        env.step(act)
        assert not env.game_over()

def viz_objs():
    import pydot
    # env = FrotzEnv("../roms/tw-treasure-hunter_level25-v0_oENpK7S9HeYksNp6HqjBf7E3T3g8.z8", seed=6)
    # env = FrotzEnv("/home/matthew/Desktop/textworld_games/tw-treasure-hunter_level1-v0_E5gBjvfVFkknFx1JF22xuaDRIqgW.z8", seed=6)
    # env = FrotzEnv("/home/matthew/Desktop/textworld_games/tw-treasure-hunter_level11-v0_RjODmqiKHxmpSPWrF3x2FpLgTVkd.z8", seed=6)
    env = FrotzEnv("/home/matthew/Desktop/textworld_games/tw-treasure-hunter_level17-v0_WMjpNbFBU25VHGOBUl38fPoYUkR0.z8", seed=6)
    print(env.reset())
    obs, score, done, _ = env.step('look')
    world_objs = env.get_world_objects()
    for o in world_objs:
        print(o)
    print("Player Obj {}".format(env.get_player_object()))
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

#test_textworld()
#find_moves()
#find_score()
viz_objs()
