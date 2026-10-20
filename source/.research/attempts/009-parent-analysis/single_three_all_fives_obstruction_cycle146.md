# A local obstruction: no even triangle family with degrees (3,5^9)

Let F be a set of distinct three-element subsets of a ten-element vertex
set. Suppose every two-element subset occurs in an even number of members
of F. Then the vertex degrees of F cannot be one 3 and nine 5s.

For a vertex v, its link is the simple graph whose edges ab correspond to
faces vab. Pair parity says every link vertex has even degree. A nonempty
simple even graph with at most five edges is a single triangle, quadrangle,
or pentagon. Indeed a shortest cycle has at least three edges; removing
its edges leaves another even graph, which if nonempty needs at least
three further edges. Thus degrees one or two cannot occur in a link.

Assume F has the claimed degree sequence, and let v have degree three.
Its link is the triangle abc. Symmetric difference with the four faces of
the tetrahedron vabc preserves all pair parities and removes v. If abc
was a face, each of a,b,c would now have degree two, a contradiction.
Therefore abc was absent. The new family F' contains abc and has degree
four on a,b,c and degree five on six further vertices. It has 14 faces.

Every nonempty link of F' is a C4 or C5. Hence every used pair has exactly
two incident faces. Write abx, bcy, caz for the second faces at ab,bc,ca.
The vertices x,y,z are outside abc. They are pairwise distinct. For
example, x=z would make the degree-four link at a contain the triangle
on b,c,x and just one further edge, which is not even. The other two
equalities give the same contradiction at b or c.

In the C4 link at a, the three edges bc,bx,cz force the edge xz.
Similarly the links at b and c force xy and yz. Consequently F' contains
the seven faces abc,abx,bcy,caz,axz,bxy,cyz. Together with xyz these are
the boundary of an octahedron, so toggling all eight preserves pair parity.
All faces incident to a,b,c are precisely the listed four at each vertex;
the toggle therefore removes a,b,c entirely. If xyz was already present,
each of x,y,z would lose four faces and have degree one, impossible.
Thus xyz was absent and is added. Each of x,y,z now has degree three.

The resulting family F'' has six vertices, eight faces, and degree sequence
(3,3,3,5,5,5). Each degree-five vertex has a C5 link and therefore is
adjacent to all five other vertices. Each degree-three vertex is consequently
adjacent to all three degree-five vertices. Its triangular link leaves no
other neighbors. It lies in three faces, each containing that degree-three
vertex and two degree-five vertices. These nine faces, three for each of
the degree-three vertices, are distinct. This contradicts the total of
eight faces, proving the assertion.

The proof uses only simple faces, pair parity, and local degrees. It assumes
neither connectedness nor a surface classification. The script
`verify_single_three_lemma_controls.py` exhausts the terminal six-vertex
cycle space and all possible even links of sizes three through five on
nine vertices, with nonempty positive controls. These finite checks support
the local steps; the deduction above supplies the ten-vertex proof.
