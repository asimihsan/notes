# Title: FSM Optimization
#
# Challenge Problem: 2 Stars
#
# Lexical analyzers are implemented using finite state machines generated
# from the regular expressions of token definition rules. The performance
# of a lexical analyzer can depend on the size of the resulting finite
# state machine. If the finite state machine will be used over and over
# again (e.g., to analyze every token on every web page you visit!), we
# would like it to be as small as possible (e.g., so that your webpages
# load quickly). However, correctness is more important than speed: even
# an optimized FSM must always produce the right answer.
#
# One way to improve the performance of a finite state machine is to make
# it smaller by removing unreachable states. If such states are removed,
# the resulting FSM takes up less memory, which may make it load faster or
# fit better in a storage-constrained mobile device.
#
# For this assignment, you will write a procedure nfsmtrim that removes
# "dead" states from a non-deterministic finite state machine. A state is
# (transitively) "dead" if it is non-accepting and only non-accepting
# states are reachable from it. Such states are also called "trap" states:
# once entered, there is no escape. In this example FSM for r"a*" ...
#
# edges = { (1,'a') : [1] ,
#           (1,'b') : [2] ,
#           (2,'b') : [3] ,
#           (3,'b') : [4] }
# accepting = [ 1 ]
#
# ... states 2, 3 and 4 are "dead": although you can transition from 1->2,
# 2->3 and 3->4 on "b", you are doomed to rejection if you do so.
#
# You may assume that the starting state is always state 1. Your procedure
# nfsmtrim(edges,accepting) should return a tuple (new_edges,new_accepting)
# corresponding to a FSM that accepts exactly the same strings as the input
# FSM but that has all dead states removed.
#
# Hint 1: This problem is tricky. Do not get discouraged.
#
# Hint 2: Think back to the nfsmaccepts() procedure from the "Reading
# Machine Minds" homework problem in Unit 1. You are welcome to reuse your
# code (or the solution we went over) to that problem.
#
# Hint 3: Gather up all of the states in the input machine. Filter down
# to just those states that are "live". new_edges will then be just like
# edges, but including only those transitions that involve live states.
# new_accepting will be just like accepting, but including only those live
# states.

import operator

def nfsmtrim(edges, accepting):
    all_states = sorted(list(set([elem[0] for elem in edges] + accepting)))
    live_states = set([state for state in all_states
                       if is_live_state(state, all_states, edges, accepting)])
    #print "live_states: %s" % live_states

    # -------------------------------------------------------------------------
    # only edges pointing to live states are kept, because the rest are
    # pointless. see `is_live_state` for defition of liveness.
    # -------------------------------------------------------------------------
    new_edges = {}
    for ((state, letter), next_states) in edges.iteritems():
        live_next_states = [next_state for next_state in next_states
                            if next_state in live_states]
        if len(live_next_states) > 0:
            new_edges[(state, letter)] = live_next_states
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    #   Only accepting states that are live and have incoming edges are kept.
    #   -   If an accepting state isn't live then it probably has incoming
    #       and/or edges in such a way that no live states are reached.
    #   -   If an accepting state has no incoming edges then it can never
    #       be transitioned to.
    # -------------------------------------------------------------------------
    all_new_states = set()
    for ((_, _), next_states) in new_edges.iteritems():
        all_new_states |= set(next_states)
    new_accepting = [state for state in accepting
                     if state in live_states and
                     state in all_new_states]
    # -------------------------------------------------------------------------

    return (new_edges, new_accepting)

def is_live_state(state, all_states, edges, accepting, visited=None):
    """Is this state live? i.e. is it, or does it eventually
    transition to via any path, an accepting state?

    -   If it is an accepting state then it is live.
    -   If it is not in all_states it does not have any outbound
        edges. As this cannot be an accepting state, given above,
        it cannot be live.
    -   Else, via every edge leaving this state, visit child
        nodes.
        -   If any child node is live then this node is
        live.
        -   If no child nodes are live then this node is
        not live.
    """
    #print "is_live_state entry. state: %s, visited: %s" % (state, visited)

    # -------------------------------------------------------------------------
    #   Initialize variables.
    # -------------------------------------------------------------------------
    if visited is None:
        visited = []
    # -------------------------------------------------------------------------

    if state in accepting:
        #print "is_live_states. state: %s, visited: %s. in accepting so return True" % (state, visited)
        return True
    if state not in all_states:
        return False
        #print "is_live_states. state: %s, visited: %s. not in all states so return False" % (state, visited)
    for ((edge_state, edge_letter), edge_next_states) in edges.iteritems():
        if edge_state != state:
            continue
        for next_state in edge_next_states:
            if next_state not in visited:
                visited.append(next_state)
                result = is_live_state(next_state,
                                       all_states,
                                       edges,
                                       accepting,
                                       visited)
                if result == True:
                    #print "is_live_states. state: %s, visited: %s. next_state %s is live so return True" % (state, visited, next_state)
                    return True
    #print "is_live_states. state: %s, visited: %s. no child is live so return False" % (state, visited)
    return False

# We have included a few test cases, but you will definitely want to make
# your own.

edges1 = { (1,'a') : [1] ,
           (1,'b') : [2] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (8,'z') : [9] , }
accepting1 = [ 1 ]
(new_edges1, new_accepting1) = nfsmtrim(edges1,accepting1)
print "1"
print new_edges1 == {(1, 'a'): [1]}
print new_accepting1 == [1]

(new_edges2, new_accepting2) = nfsmtrim(edges1,[])
print "2"
print new_edges2 == {}
print new_accepting2 == []

(new_edges3, new_accepting3) = nfsmtrim(edges1,[3,6])
print "3"
print new_edges3 == {(1, 'a'): [1], (1, 'b'): [2], (2, 'b'): [3]}
print new_accepting3 == [3]

edges4 = { (1,'a') : [1] ,
           (1,'b') : [2,5] ,
           (2,'b') : [3] ,
           (3,'b') : [4] ,
           (3,'c') : [2,1,4] }
accepting4 = [ 2 ]
(new_edges4, new_accepting4) = nfsmtrim(edges4, accepting4)
print "4"
print new_edges4
print new_accepting4
print new_edges4 == {
  (1, 'a'): [1],
  (1, 'b'): [2],
  (2, 'b'): [3],
  (3, 'c'): [2, 1],
}
print new_accepting4 == [2]

edges5 = { (1, 'a') : [1],
           (1, 'b') : [2],
           (2, 'b') : [3] }
accepting5 = [3]
(new_edges5, new_accepting5) = nfsmtrim(edges5, accepting5)
print "5"
print new_edges5
print new_accepting5
print new_edges5 == {
    (1, 'a'): [1],
    (1, 'b'): [2],
    (2, 'b'): [3],
}
print new_accepting5 == [3]

