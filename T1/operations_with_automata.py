from deterministic_automaton import *
from non_deterministic_automaton import *
from regular_grammar import *
import copy

def make_nondeterministic(fa):
    if type(fa) is type(NDAutomaton(set(), set(), NDState(''))):
        return fa
    newStates = set()
    newFinalStates = set()
    for s in fa.states:
        newS = NDState(s.name, s.isAcceptance)
        newStates.add(newS)
        if s == fa.initialState:
            newInitial = newS
    for s in newStates:
        for ts in newStates:
            for oldS in fa.states:
                for t in oldS.transitions:
                    if s == oldS and t.target_state == ts:
                        s.add_transition(NDTransition(t.symbol, [ts]))
            if s.isAcceptance:
                newFinalStates.add(s)

    return NDAutomaton(newStates, newFinalStates, newInitial, fa.Σ)

def automata_union(fa1, fa2):
    nfa1 = make_nondeterministic(fa1)
    nfa2 = make_nondeterministic(fa2)

    result_Σ = list(set(fa1.Σ) | set(fa2.Σ))
    result_states = set()
    result_final_states = set()
    operand_states_1 = copy.deepcopy(list(nfa1.states))
    operand_states_2 = copy.deepcopy(list(nfa2.states))
    i = 1
    for op in operand_states_1:
        if op == nfa1.initialState:
            newName1 = 'q' + str(i)
            op.name = newName1
            i += 1
            continue
        op.name = 'q' + str(i)
        i += 1
    for op in operand_states_2:
        if op == nfa2.initialState:
            newName2 = 'q' + str(i)
            op.name = newName2
            i += 1
            continue
        op.name = 'q' + str(i)
        i += 1
    operand_states = operand_states_1 + operand_states_2
    #operand_final_states = fa1.finalStates | fa2.finalStates
    for s in operand_states:
        newS = NDState(s.name, s.isAcceptance)
        if s.name == newName1:
            nis1 = newS
        if s.name == newName2:
            nis2 = newS
        result_states.add(newS)
    for s in result_states:
        for op in operand_states:
            for t in op.ndtransitions:
                target = set()
                for ts in t.target_states:
                    for s2 in result_states:
                        if ts == s2:
                            target.add(ts)
                if s == op:
                    s.add_transition(NDTransition(t.symbol, target))
        if s.isAcceptance:
            result_final_states.add(s)

    t1 = NDTransition('&', [nis1])
    t2 = NDTransition('&', [nis2])
    newInitial = NDState('q0', nis1.isAcceptance or nis2.isAcceptance)
    newInitial.add_transition(t1)
    newInitial.add_transition(t2)

    result_states.add(newInitial)
    if newInitial.isAcceptance:
        result_final_states.add(newInitial)

    return NDAutomaton(result_states, result_final_states, newInitial, result_Σ)


def automata_complement(af1):
    waf = None
    if type(af1) is type(NDAutomaton(set(), set(), NDState(''))):
        waf = af1.determinize()
    else:
        waf = af1
    waf.complete()

    new_states = copy.deepcopy(waf.states)
    #print(new_states)
    for s in new_states:
        if s == waf.initialState:
            new_initial_state = s

    for s in new_states:
        trans = []
        for ns in new_states:
            for t in s.transitions:
                if ns == t.target_state:
                    trans.append(Transition(t.symbol, ns))
        s.transitions = trans

    nfs = [s for s in new_states if s.isAcceptance == False]
    #print(new_states)
    for s in new_states:
        s.isAcceptance = s in nfs

    return Automaton(new_states, nfs, new_initial_state, af1.Σ)

def automata_intersec(af1, af2):
    neg_fa1 = automata_complement(af1)
    neg_fa2 = automata_complement(af2)

    union = automata_union(neg_fa1, neg_fa2)
    union = union.determinize()
    union = union.minimize()
    union = union.rename_states()
    print(union)
    union = automata_complement(union)
    #union = union.rename_states()
    print(union)
    #for t in union.initialState.transitions:
        #print(t)
    #for s in union.states:
        #for t in s.transitions:
            #print(t)
    #union.remove_unreacheable_states()
    #print(union.states)

    '''print(union.process_input('aaaa'))
    print(union.process_input('aaab'))
    print(union.process_input('aaba'))
    print(union.process_input('aabb'))
    print(union.process_input('abaa'))
    print(union.process_input('abab'))
    print(union.process_input('abbb'))
    print(union.process_input('baaa'))
    print(union.process_input('baab'))
    print(union.process_input('baba'))
    print(union.process_input('babb'))
    print(union.process_input('bbaa'))
    print(union.process_input('bbab'))
    print(union.process_input('bbba'))
    print(union.process_input('bbbb'))'''

    return union
