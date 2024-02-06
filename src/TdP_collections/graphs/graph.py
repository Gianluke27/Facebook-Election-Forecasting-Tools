# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Graph:
  """Representation of a simple graph using an adjacency map."""
  __slots__ = '_outgoing', '_incoming'
  #------------------------- nested Vertex class -------------------------
  class Vertex:
    """Lightweight vertex structure for a graph."""
    __slots__ = '_element'

    def __init__(self, x):
      """Do not call constructor directly. Use Graph's insert_vertex(x)."""
      self._element = x

    def element(self):
      """Return element associated with this vertex."""
      return self._element

    def __hash__(self):         # will allow vertex to be a map/set key
      return hash(id(self))

    def __str__(self):
      return str(self._element)

  #------------------------- nested Edge class -------------------------
  class Edge:
    """Lightweight edge structure for a graph."""
    __slots__ = '_origin', '_destination', '_element'

    def __init__(self, u, v, x):
      """Do not call constructor directly. Use Graph's insert_edge(u,v,x)."""
      self._origin = u
      self._destination = v
      self._element = x

    def opposite_fast_origin(self):
      """Return the vertex that is opposite v on this edge."""
      return self._origin

    def opposite_fast_dest(self):
      """Return the vertex that is opposite v on this edge."""
      return self._destination

    def element(self):
      """Return element associated with this edge."""
      return self._element

    def set_element(self, x):
      self._element = x

    def __hash__(self):         # will allow edge to be a map/set key
      return hash( (self._origin, self._destination) )

  #------------------------- Graph methods -------------------------
  def __init__(self, directed=False):
    """Create an empty graph (undirected, by default).

    Graph is directed if optional paramter is set to True.
    """
    self._outgoing = {}
    # only create second map for directed graph; use alias for undirected
    self._incoming = {} if directed else self._outgoing

  def edges(self):
    """Return a set of all edges of the graph."""
    result = set()       # avoid double-reporting edges of undirected graph
    for secondary_map in self._outgoing.values():
      result.update(secondary_map.values())    # add edges to resulting set
    return result

  def get_edge_fast(self, u, v):
    """Return the edge from u to v, or None if not adjacent."""
    return self._outgoing[u].get(v)

  def get_incoming(self, v):
    return self._incoming[v]

  def get_outgoing(self, v):
    return self._outgoing[v]

  def incident_edges_fast(self, v):
    for edge in self._outgoing[v].values():
      yield edge

  def insert_edge_fast(self, u, v, x=None):
    e = self.Edge(u, v, x)
    self._outgoing[u][v] = e
    self._incoming[v][u] = e

  def insert_edge_fast_bidirectional(self, u, v, x=None):
    e = self.Edge(u, v, x)
    e2 = self.Edge(v, u, x)
    self._outgoing[u][v] = e
    self._incoming[u][v] = e2
    self._outgoing[v][u] = e2
    self._incoming[v][u] = e

  def remove_vertex(self, v: Vertex):
    to_remove = list(e for e in self.incident_edges(v))

    for e in to_remove:
      self.remove_edge(e)

    del self._outgoing[v]
    del self._incoming[v]

  def insert_vertex_directed(self, x=None):
    v = self.Vertex(x)
    self._outgoing[v] = {}
    self._incoming[v] = {}
    return v

  def remove_edge_fast(self, u,v):
    """Remove a Edge e.
    """
    del self._outgoing[u][v]
    del self._incoming[v][u]


