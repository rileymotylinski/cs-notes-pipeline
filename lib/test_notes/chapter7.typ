= Matrices
- only 2 dimensional Matrices
- relationships between valeus in rows vs values in coloumns
- an item a column $n$, row $n$ describes $m$'s relationship to $n$.
- you can add Matrices

== Product of two Matrices
- n has to equal k between two matrices
- multiply all the row/column elements and add them together. That is one term in the resulting matrix.
- you can also square a matrix
=== Identity matrix
- nxn matrix where everything is 0's except the diagonal, which is one.
- $I_0$
- $A I_n = I_m A = A$

== Transpose of a matrix
- interchange the rows and columns of the matrix to go from an mxn to an nxm matrix
- a matrix is *symmetric* if $A = A^T$. Or, are they symmetric about their diagonal.

== join/meet of two matrices
- this is for 1-0 matrices
- or-ing/and-ing two matrices, respectively
== Boolean Product of two matrices
- anding for inside terms and oring for outside terms.
- same thing as multiplication, but with boolean operations
- multiply each row in the first matrix by the column in the second matrix
- you can also put powers to boolean mtrices; it just does the same thing


== Zero-One Matrice
- used to represent relationship between element i and element j

= Relations
- numeric elements can be understood furhter by relating them together
* Definition 1 * - a binary relation from A to B is a subset of $A x B$ (that is , the cartesian product)
- cartesian product is $ A x B {(a,b) | a in A, b in B} $
- total possible combinations is $|n| times |m|$
- a relation is a generalization of a function
- functions can only have 1 element from the domain to one element in the codomain

== Relation Properties
=== Reflexivity
- a relation is reflexive if $(a,a) in R forall a in A$. Every element in the domain is mapped to itself in the codomain.
- a relation is irreflexive if $(a,a) in.not R forall a in A$. No element is related to itself.
- a relation can be neither reflexive nor irreflexive, but not both at the same time.

=== Symmetry
- a relation is symmetric if $forall a,b in A, (a,b) in R ==> (b,a) in R$
- a relation is antisymmetric if $forall a,b in A, ((a,b) in R and (b,a) in R) ==> a=b$
- another definition is $forall a,b in A, ((a,b) in R and a eq.not b) ==> (b,a) in.not R$
- basically, only unique pair flips from the first set should not  be in the second set.
- a relation could be neither symmetric or antisymmetric
- these relations are not mutually exclusive


=== Transitivity
- a relation is transitive if $forall a,b,c in A ((a,b) in R and (b,c) in R ==> (a,c) in R)$
- kind of like taking the "book end pair" of two elements

== Combing Relations
- you can combine relations similar to function compositions $S compose R$
this is a change

- $R_>= union R_<=$ all numbers $>=$ or $<=$
- $inter$ and
- relation composition: reverse domain and codomain. Compose two complex relations to represent some complex relation
- databases are simply defined as relations
- n-nary relations, as oposed to binary relations, are the bassi for a cs application called databases
- databses are n-tuples of fields
- just giving relations to find other relations


== Back to Binary Relations
- binary relations can be represented as a matrix
- a relation is reflexive if tits matrix representation is reflexive (diagonal is all 1s)
- same with irreflexivity (diagonal is all 0's')
Symmetric - opposite values are mirrored
- anti symmetrix - opposite values about the diagonal are opposite. (0,0) is fine, but (1,0) or (0,1) is not allowed

- digraphs - directed graph. Using each element in a as a vertex in a graph and each order pari as a directed edge from a to book
- can you represent a digraph with a set

== Graphs
- reflexive (all elemenrts have loop)/irreflxive (absence of loops), etc. can be inferred given a visual representation of a graph

== Advanced relations
*Equivalence* - relation which is _reflexive_, _symmetric_, _transitive_. This is denoted with a "~", e.g. $a tilde b$:

== Equivalence Classes
- Let $R$ be an equivalence relation on a set $A$. The set of all elements that are related to an elelemnt $a in A$ is called the _equivalence class_ of a.
Example:

$ R = {(a,b) | a eq.triple b (mod 2)} $

So all even numbers form an equivalence class, as well as all odd numbers.






 









































