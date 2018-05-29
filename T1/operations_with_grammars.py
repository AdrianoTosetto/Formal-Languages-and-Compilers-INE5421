from deterministic_automaton import *
from non_deterministic_automaton import *
from regular_grammar import *
import copy

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
            'O', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def grammar_union(gr1, gr2):
    hasEpsilon = False
    oldProds1 = copy.deepcopy(gr1.productions)
    initial1 = copy.deepcopy(gr1.productions[0].leftSide)
    oldNonTerminals1 = set()
    oldProds2 = copy.deepcopy(gr2.productions)
    initial2 = copy.deepcopy(gr2.productions[0].leftSide)
    oldNonTerminals2 = set()
    visited = set()
    count = 0
    for p1 in oldProds1:
        if p1.rightSide is '&':
            hasEpsilon = True
            oldProds1_1 = oldProds1 - p1
            break
        oldProds1_1 = oldProds1
    oldProds1 = oldProds1_1
    for p2 in oldProds2:
        if p2.rightSide is '&':
            hasEpsilon = True
            oldProds2_1 = oldProds2 - p1
            break
        oldProds2_1 = oldProds2
    oldProds2 = oldProds2_1
    for p1 in gr1.productions:
        oldNonTerminals1.add(p1.leftSide)
        if len(p1.rightSide) > 1:
            oldNonTerminals1.add(p1.rightSide[-1])
    for p2 in gr2.productions:
        oldNonTerminals2.add(p2.leftSide)
        if len(p2.rightSide) > 1:
            oldNonTerminals2.add(p2.rightSide[-1])
    #---------------------------------------------------------------------------
    for n1 in oldNonTerminals1:
        for p1 in oldProds1:
            if p1.leftSide == n1:
                if n1 == initial1:
                    initial1 = str(count)
                p1.leftSide = str(count)
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == n1:
                p1.rightSide = p1.rightSide[0] + str(count)
        count += 1
    count1 = count
    for n2 in oldNonTerminals2:
        for p2 in oldProds2:
            if p2.leftSide == n2:
                if n2 == initial2:
                    initial2 = str(count)
                p2.leftSide = str(count)
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == n2:
                p2.rightSide = p2.rightSide[0] + str(count)
        count += 1
    count2 = count
    #---------------------------------------------------------------------------
    for n1 in range(count1):
        for p1 in oldProds1:
            if p1.leftSide == str(n1):
                if str(n1) == initial1:
                    initial1 = alphabet[n1]
                p1.leftSide = alphabet[n1]
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == str(n1):
                p1.rightSide = p1.rightSide[0] + alphabet[n1]
    for n2 in range(count2):
        for p2 in oldProds2:
            if p2.leftSide == str(n2):
                if str(n2) == initial2:
                    initial2 = alphabet[n2]
                p2.leftSide = alphabet[n2]
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == str(n2):
                p2.rightSide = p2.rightSide[0] + alphabet[n2]

    newProds = []

    for p1 in oldProds1:
        if p1.leftSide == initial1:
            newProds.append(Production('S', p1.rightSide))
    for p2 in oldProds2:
        if p2.leftSide == initial2:
            newProds.append(Production('S', p2.rightSide))

    newProds = newProds + oldProds1 + oldProds2

    return Grammar(newProds, gr1.name + " ∪ " + gr2.name)

def grammar_concatenation(gr1, gr2):
    hasEpsilon = False
    oldProds1 = copy.deepcopy(gr1.productions)
    initial1 = copy.deepcopy(gr1.productions[0].leftSide)
    oldNonTerminals1 = set()
    oldProds2 = copy.deepcopy(gr2.productions)
    initial2 = copy.deepcopy(gr2.productions[0].leftSide)
    oldNonTerminals2 = set()
    visited = set()
    count = 0
    for p2 in oldProds2:
        if p2.rightSide is '&':
            hasEpsilon = True
            oldProds2_1 = oldProds2 - p1
            break
        oldProds2_1 = oldProds2
    oldProds2 = oldProds2_1
    for p1 in gr1.productions:
        oldNonTerminals1.add(p1.leftSide)
        if len(p1.rightSide) > 1:
            oldNonTerminals1.add(p1.rightSide[-1])
    for p2 in gr2.productions:
        oldNonTerminals2.add(p2.leftSide)
        if len(p2.rightSide) > 1:
            oldNonTerminals2.add(p2.rightSide[-1])
    #---------------------------------------------------------------------------
    for n1 in oldNonTerminals1:
        for p1 in oldProds1:
            if n1 == initial1:
                continue
            if p1.leftSide == n1:
                p1.leftSide = str(count)
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == n1:
                p1.rightSide = p1.rightSide[0] + str(count)
        count += 1
    count1 = count
    for n2 in oldNonTerminals2:
        for p2 in oldProds2:
            if p2.leftSide == n2:
                if n2 == initial2:
                    initial2 = str(count)
                p2.leftSide = str(count)
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == n2:
                p2.rightSide = p2.rightSide[0] + str(count)
        count += 1
    count2 = count
    #---------------------------------------------------------------------------
    for n1 in range(count1):
        for p1 in oldProds1:
            if p1.leftSide == str(n1):
                p1.leftSide = alphabet[n1]
            if len(p1.rightSide) > 1 and p1.rightSide[-1] == str(n1):
                p1.rightSide = p1.rightSide[0] + alphabet[n1]
    for n2 in range(count2):
        for p2 in oldProds2:
            if p2.leftSide == str(n2):
                if str(n2) == initial2:
                    initial2 = alphabet[n2]
                p2.leftSide = alphabet[n2]
            if len(p2.rightSide) > 1 and p2.rightSide[-1] == str(n2):
                p2.rightSide = p2.rightSide[0] + alphabet[n2]
    if hasEpsilon:
        for p1 in oldProds1:
            if len(p1.rightSide) == 1:
                oldProds1.append(Production(p1.leftSide, p1.rightSide + initial2))
    else:
        for p1 in oldProds1:
            if len(p1.rightSide) == 1:
                p1.rightSide = p1.rightSide + initial2

    newProds = oldProds1 + oldProds2

    return Grammar(newProds, gr1.name + "." + gr2.name)
