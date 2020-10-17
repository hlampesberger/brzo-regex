from graphviz import Digraph
from brzo.parse import parse
import brzo.regex as br

def get_dfa(alphabet, re):
    re0 = parse(re).approximate()
    queue = [re0]
    states = set()
    transition = dict()
    while queue:
        re = queue.pop()
        states.add(re)
        for a in alphabet:
            next_re = re.derivative(a).approximate()
            transition[re, a] = str(next_re)
            if next_re not in states:
                queue.append(next_re)

    dot = Digraph()
    for q in states:
        if q.nullable():
            dot.node(str(q), shape="doubleoctagon")
        else:
            dot.node(str(q))
    dot.node("START", "", shape="none")
    dot.edge("START", str(re0))

    import collections
    edges = collections.defaultdict(set)

    for (q, a), qn in transition.items():
        edges[q, qn].add(a)

    for (q, qn), A in edges.items():
        dot.edge(str(q), str(qn), label=', '.join(sorted(A)))
    return dot

def get_dfa_without_error_state(alphabet, re):
    re0 = parse(re).approximate()
    queue = [re0]
    states = set()
    transition = dict()
    while queue:
        re = queue.pop()
        states.add(re)
        if not isinstance(re, br.EmptySet):
            for a in alphabet:
                next_re = re.derivative(a).approximate()
                if not isinstance(next_re, br.EmptySet):
                    transition[re, a] = str(next_re)
                    if next_re not in states:
                        queue.append(next_re)

    dot = Digraph()
    for q in states:
        if q.nullable():
            dot.node(str(q), shape="doubleoctagon")
        else:
            dot.node(str(q))
    dot.node("START", "", shape="none")
    dot.edge("START", str(re0))

    import collections
    edges = collections.defaultdict(set)

    for (q, a), qn in transition.items():
        edges[q, qn].add(a)

    for (q, qn), A in edges.items():
        dot.edge(str(q), str(qn), label=', '.join(sorted(A)))
    return dot