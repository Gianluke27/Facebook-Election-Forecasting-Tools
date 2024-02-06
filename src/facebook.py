import random as ran
import TdP_collections.graphs.graph as graph

def BFS_final(g, s, discovered):
  level = [s]                        # first level includes only s
  while len(level) > 0:
    next_level = []                  # prepare to gather newly found vertices
    for u in level:
      for e in g.incident_edges_fast(u):  # for every outgoing edge from u
        v = e.opposite_fast_dest()
        if v not in discovered:      # v is an unvisited vertex
          discovered[v] = e          # e is the tree edge that discovered v
          next_level.append(v)       # v will be further considered in next pass
    level = next_level

def BFS_u_to_v_complete(G, u, V_t):
  forest = {u: None}
  found, t_e = BFS_u_to_v(G, forest, u, V_t)
  return forest, found, t_e

def BFS_u_to_v(g, discovered, source, V_t):
  level = [source]
  while len(level) > 0:
    next_level = []
    for u in level:
      for e in g.incident_edges_fast(u):
        opposite = e.opposite_fast_dest()
        if opposite in V_t:
            discovered[opposite] = e
            next_level.append(opposite)
            return True, opposite
        if opposite.element() == -1:
            continue
        if opposite not in discovered:         # v is an unvisited vertex
          discovered[opposite] = e             # e is the tree edge that discovered v
          next_level.append(opposite)
    level = next_level               # relabel 'next' level to become current
  return False, None

def to_move_greedy_D(D, all_vertex, source):
    int_cut = 0
    ext_cut = 0
    for v in all_vertex[source]:
        if v in D:
            int_cut += all_vertex[source][v]
        else:
            ext_cut += all_vertex[source][v]
    return True if int_cut > ext_cut else False

def to_move_greedy_R(R, all_vertex, source):
    int_cut = 0
    ext_cut = 0
    for v in all_vertex[source]:
        if v in R:
            int_cut += all_vertex[source][v]
        else:
            ext_cut += all_vertex[source][v]
    return True if int_cut > ext_cut else False

def facebook_enmy(V, E):
    R = set()
    D = set()
    all_vertex = {}

    for vertex in V:
        all_vertex[vertex] = {}
        if (len(R) - len(D) >= 2):
            D.add(vertex)
        elif (len(R) - len(D) <= 2):
            R.add(vertex)
        else:
            if ran.randint(0, 1) == 1:
                R.add(vertex)
            else:
                D.add(vertex)

    for e in E:
        all_vertex[e[0]][e[1]] = E[e]
        all_vertex[e[1]][e[0]] = E[e]

    for vertex in V:
        if (vertex in R):
            if to_move_greedy_R(R, all_vertex, vertex):
                R.remove(vertex)
                D.add(vertex)
        else:
            if to_move_greedy_D(D, all_vertex, vertex):
                D.remove(vertex)
                R.add(vertex)

    return D,R

def buildFlowNet(V: dict, E:dict):
    G = graph.Graph(directed=True)

    vertex = {"s": G.insert_vertex_directed("s"), -1: G.insert_vertex_directed(-1)}

    for v in V:
        vertex[v] = G.insert_vertex_directed(v)
        el_uno, el_due = V[v]
        if not (el_uno == el_due):
            if el_uno > el_due:
                G.insert_edge_fast(vertex["s"], vertex[v], el_uno - el_due)
            else:
                G.insert_edge_fast(vertex[v], vertex[-1], el_due - el_uno)

    for e in E:
        val = E[e]
        if (val != 0):
            G.insert_edge_fast_bidirectional(vertex[e[0]], vertex[e[1]], val)

    return G, vertex

def Augment(G: graph.Graph, path: list, forest: dict):
    bottleneck = forest[path[1]].element()
    for v in path:
        if forest[v] is None:
            pass
        elif forest[v].element() < bottleneck:
            bottleneck = forest[v].element()

    if bottleneck == 0:
        return bottleneck

    for vert in path:
        e = forest[vert]
        if e is not None:
            vert2 = e.opposite_fast_origin()
            val_e = e.element() - bottleneck
            if val_e == 0:
                G.remove_edge_fast(vert2, vert)
            else:
                e.set_element(val_e)
            if(vert.element() != -1 and vert2.element() != "s"):
                e2 = G.get_edge_fast(vert, vert2)
                if e2 is None:
                    G.insert_edge_fast(vert, vert2, bottleneck)
                else:
                    e2.set_element(e2.element() + bottleneck)

    return bottleneck

def construct_path_s_t(u, v, discovered):
  path = []                        # empty path by default
  if v in discovered:
    path.append(v)
    walk = v
    while walk is not u:
      e = discovered[walk]         # find edge leading to walk
      if e is None:
          break
      parent = e.opposite_fast_origin()
      path.append(parent)
      walk = parent
  return path

def maxFlow(G: graph.Graph, V: dict):
    t_dict = G.get_incoming(V[-1])
    s_dict = G.get_outgoing(V["s"])

    source = V["s"]
    tank = V[-1]

    s_dict_copy = s_dict.copy()

    flag_no_tank = False

    for s_e in s_dict_copy:
        e_s_dict = s_dict.get(s_e)
        while True:
            if len(t_dict) == 0:
                flag_no_tank = True
                break
            if s_e not in s_dict:
                break
            forest, found, t_e = BFS_u_to_v_complete(G, s_e, t_dict)
            if not found:
                break
            forest[source] = None
            forest[s_e] = e_s_dict
            forest[tank] = G.get_edge_fast(t_e, tank)

            path = construct_path_s_t(source, tank, forest)
            Augment(G, path, forest)
        if flag_no_tank:
            break

    R = set()
    D = set()

    if flag_no_tank:
        del V["s"]
        del V[-1]
        for vertex in V:
            D.add(vertex)
        return D,R

    forest = {}
    forest[V["s"]] = None  # u will be a root of a tree
    BFS_final(G, V["s"], forest)

    del V["s"]
    del V[-1]

    for vertex in V:
        if V[vertex] in forest:
            D.add(vertex)
        else:
            R.add(vertex)

    return D,R

def facebook_friend(V: dict, E:dict):
    G, vertex = buildFlowNet(V,E)
    return maxFlow(G, vertex)