from deterministic_automaton import *
from non_deterministic_automaton import *
from regular_grammar import *
import copy

def make_nondeterministic(fa):
    if type(fa) is NDAutomaton:
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
                if s == op:
                    s.add_transition(NDTransition(t.symbol, t.target_states))
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
    if type(af1) is NDAutomaton:
        waf = af1.determinize()
    else:
        waf = af1
    waf.complete()

    new_states = copy.deepcopy(waf.states)
    for s in new_states:
        if s == waf.initialState:
            new_initial_state = s

    '''for s in af1.states:
        for t in s.transitions:
            new_states.add(State(t.target_state.name))'''

    '''for s in af1.states:
        for ncs in new_states:
            if s == ncs:
                for t in s.transitions:
                    for ncs1 in new_states:
                        if ncs1 == t.target_state:
                            ncs.add_transition(Transition(t.symbol, ncs1))'''
    nfs = [s for s in new_states if s.isAcceptance == False]
    for s in new_states:
        s.isAcceptance = not s.isAcceptance
    return Automaton((new_states), (nfs), new_initial_state, af1.Σ)

def automata_intersec(af1, af2):
    neg_fa1 = af1#automata_complement(af1)
    neg_fa2 = af2#automata_complement(af2)

    print(neg_fa1)
    print(neg_fa2)

    union = automata_union(neg_fa1, neg_fa2)#.determinize()#.minimize()
    print(union)
    union = union.determinize()
    print(union)
    #union.rename_states()
    print(union)
    print(type(union.currentState))
    for s in union.states:
        for t in s.transitions:
            for st in t.target_state.transitions:
                print(str(t.target_state) + " + " + str(st))
    print(union.process_input(''))
    print(union.process_input('a'))
    print(union.process_input('b'))
    print(union.process_input('aa'))
    print(union.process_input('ab'))
    print(union.process_input('ba'))
    print(union.process_input('bb'))
    print(union.process_input('aaa'))
    print(union.process_input('aab'))
    print(union.process_input('aba'))
    print(union.process_input('abb'))
    print(union.process_input('baa'))
    print(union.process_input('bab'))
    print(union.process_input('bba'))
    print(union.process_input('bbb'))

    #return automata_complement(union)
