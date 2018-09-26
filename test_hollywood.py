from jericho import *

walkthrough = 'n/open mailbox/take all from mailbox/examine status line/examine business card/examine yellow paper/open door/n/turn on torch/n/examine model/press green/PRESS GREEN/PRESS GREEN/PRESS BLACK/PRESS BLACK/PRESS WHITE/PRESS WHITE/PRESS GREEN/PRESS GREEN/PRESS GREEN/PRESS BLUE/PRESS  BLACK/PRESS GREEN/PRESS GREEN/PRESS GREEN/PRESS GREEN/PRESS RED/PRESS RED/PRESS RED/TAKE RING/EXAMINE RING/W/TAKE THIN PAPER/EXAMINE THIN PAPER/W/TAKE MATCHBOX/EXAMINE IT/DOWN/EXAMINE COMPUTER/OPEN CLOSET DOOR/S/TAKE BLUE CARD AND EXAMINE IT/N/UP/E/S/EXAMINE FIREPLACE/ENTER FIREPLACE/TAKE BRICK/DROP BRICK/TAKE INDIGO CARD/E/EXAMINE RED STATUE/EXAMINE WHITE STATUE/EXAMINE BLUE STATUE/DROP ALL EXCEPT TORCH/E/E/EXAMINE PAINTING/LOOK BEHIND PAINTING/TAKE GREEN CARD/EXAMINE SAFE/TURN DIAL RIGHT 3/TURN DIAL LEFT 7/TURN DIAL RIGHT 5/open safe/TAKE GRATER/EXAMINE IT/W/N/E/E/TAKE YELLOW CARD/S/TAKE SLIDE/EXAMINE SLIDE PROJECTOR/PUT SLIDE IN SLIDE PROJECTOR/TURN ON SLIDE PROJECTOR/EXAMINE SCREEN/FOCUS SLIDE PROJECTOR/EXAMINE SCREEN/TAKE FILM/EXAMINE FILM PROJECTOR/REMOVE  LENS CAP/PUT FILM IN FILM PROJECTOR/TURN ON FILM PROJECTOR/EXAMINE SCREEN'
solution = walkthrough.split('/')

def test_hollywood():
    env = FrotzEnv("../../TextWorld-baselines/games/hollywood.z3", seed=6)
    env.reset()
    for act in solution:
        print("{} {}".format(act, env.step(act)))
        loc = env.get_player_location()
        print("Loc {}-{}".format(loc.name, loc.num))
        for i in env.get_inventory():
            print("  {}-{}".format(i.name, i.num))
        print('')

def test_max_score():
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
    assert env.get_max_score() == 150

# def test_load_save_file():
#     fname = 'hollywood.qzl'
#     env = FrotzEnv("../roms/hollywood.z3", seed=6)
#     env.reset()
#     for act in solution[:5]:
#         orig_obs, _, _, _ = env.step(act)
#     if os.path.exists(fname):
#         os.remove(fname)
#     env.save(fname)
#     orig_obs, _, _, _ = env.step('look')
#     # orig_obs = orig_obs[orig_obs.index('The inside'):]
#     for act in solution[5:10]:
#         new_obs, _, _, _ = env.step(act)
#     assert new_obs != orig_obs
#     env.load(fname)
#     restored, _, _, _ = env.step('look')
#     # restored = restored[restored.index('The inside'):]
#     assert restored == orig_obs
#     if os.path.exists(fname):
#         os.remove(fname)

# TODO: Fix Illegal Opcode on RESTORE
# def test_load_save_str():
#     env = FrotzEnv("../roms/hollywood.z3", seed=6)
#     env.reset()
#     for act in solution[:5]:
#         orig_obs, _, _, _ = env.step(act)
#     save = env.save_str()
#     orig_obs, _, _, _ = env.step('look')
#     # orig_obs = orig_obs[orig_obs.index('The inside'):]
#     for act in solution[5:10]:
#         new_obs, _, _, _ = env.step(act)
#     assert new_obs != orig_obs
#     env.load_str(save)
#     restored, _, _, _ = env.step('look')
#     # restored = restored[restored.index('The inside'):]
#     assert restored == orig_obs, "Orig: {}, Restored {}".format(orig_obs, restored)

def manual_score(env, obs):
    obs, _, _, _ = env.step('score')
    print(obs)
    pattern = 'Your score is '
    start = obs.index(pattern)
    end = obs.index('points out of ')
    score = int(obs[start+len(pattern):end])
    return score

def manual_moves(env, obs):
    obs, _, _, _ = env.step('score')
    print(obs)
    a = '150, in '
    idx = obs.index(a)
    return int(obs[idx+len(a):obs.index(' move',idx)])

def test_score_detection():
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
    env.reset()
    for act in solution:
        obs, score, done, _ = env.step(act)
        assert manual_score(env, obs) == score

def test_move_detection():
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
    env.reset()
    for idx, act in enumerate(solution[:30]):
        obs, score, done, info = env.step(act)
        assert info['moves'] == manual_moves(env, obs)

def test_inventory():
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
    env.reset()
    for act in solution:
        env.step(act)
    inv = env.get_inventory()
    inv_names = [o.name for o in inv]
    assert 'lens cap' in inv_names

def find_score():
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
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
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
    env.reset()
    old_ram = env.get_ram()
    d = {}
    cnt = 0
    for act in solution:
        cnt += 1
        obs, _, _, _ = env.step(act)
        moves = manual_moves(env, obs)
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
        if value/float(cnt) > .9:
            print("{}: {}".format(key, value/float(cnt)))

# def test_world_change():
#     env = FrotzEnv("../roms/hollywood.z3", seed=6)
#     env.reset()
#     for act in solution:
#         obs, _, _, _ = env.step(act)
#         assert env.world_changed(),\
#             "Expected world change: Act: \"{}\" Obs: \"{}\" Diff: {}"\
#             .format(act, obs, env.get_world_diff())

def test_game_over():
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
    env.reset()
    for act in solution:
        env.step(act)
        assert not env.game_over()

def viz_objs():
    import pydot
    env = FrotzEnv("../roms/hollywood.z3", seed=6)
    print(env.reset())
    obs, score, done, _ = env.step('look')
    # world_objs = [env.get_object(i) for i in range(241)]
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

test_hollywood()
#find_moves()
#find_score()
#viz_objs()
#test_load_save_file()
#test_load_save_str()
