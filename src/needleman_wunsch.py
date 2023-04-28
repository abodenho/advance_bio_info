from itertools import combinations
import numpy as np
import sys

""" Similarity matrix
    A   G   C   T
A    1  -1  -1  -1
G   -1   1  -1  -1
C   -1  -1   1  -1
T   -1  -1  -1   1
"""

score = {'match': 2, 'mismatch': -1, 'gap':-2, 'extend':-1}

def get_score(): return score

def _generator(string):
    for s in string:
        yield s

def _aligned_score(aligned_char, char):
    return sum([score['match'] if c==char else score['mismatch'] for c in aligned_char])


def _compute_matrix(aligned_seqs, new_seq):
    """
    Compute Needleman-Wunsch matrix
    """
    # Init score matrix (cumulative gap penality for first row and column, else 0)
    matrix = [[(a+b)*score['extend'] if a==0 or b==0 else 0 for b in range(1+len(new_seq))] for a in range(1+len(aligned_seqs[0]))]
    # Init direction matrix to keep track of the best direction
    directions = [[(0,0) for b in range(1+len(new_seq))] for a in range(1+len(aligned_seqs[0]))]

    # Fill the matrices
    for i, aligned_char in enumerate(zip(*aligned_seqs)):
        for j, char in enumerate(new_seq):
            # (-1,-1) = TOP_LEFT
            from_top_left = matrix[i][j] + _aligned_score(aligned_char, char)
            # (0,-1) = TOP
            from_top =  matrix[i][j+1] + (score['extend'] if directions[i][j+1]==(0,-1) else score['gap'])
            # (-1,0) = LEFT
            from_left = matrix[i+1][j] + (score['extend'] if directions[i+1][j]==(-1,0) else score['gap'])

            # Keep track of best direction
            if from_top_left >= from_top and from_top_left >= from_left:
                matrix[i+1][j+1] = from_top_left
                directions[i+1][j+1] = (-1,-1)
            elif from_top >= from_top_left and from_top >= from_left:
                matrix[i+1][j+1] = from_top
                directions[i+1][j+1] = (0,-1)
            elif from_left >= from_top_left and from_left >= from_top:
                matrix[i+1][j+1] = from_left
                directions[i+1][j+1] = (-1,0)
            else:
                print("ERROR")
                sys.exit()

    return directions

def _find_path(aligned_seqs, new_seq):
    """
    Find alignement (best path in Needleman-Wunsch)
    """
    directions = _compute_matrix(aligned_seqs, new_seq)
    i = len(directions[0])-1
    j = len(directions)-1
    path = []
    while i!=0 and j!=0:
        dir = directions[j][i]
        path.append(dir)
        i += dir[0]
        j += dir[1]
    path.reverse()
    return path

def compute_score(seqs): # TODO optimize with memoisation
    rep = 0
    for seq_A, seq_B in combinations(seqs, 2):
        for a, b in zip(seq_A, seq_B):
            if a=='-' or b=='-':
                rep += score['gap']
            elif a==b:
                rep += score['match']
            else:
                rep += score['mismatch']
    return rep

def needleman_wunsch(profile, seq):
    """
    EXAMPLE with "score = {'match': 2, 'mismatch': -1, 'gap':-2, 'extend':-1}"

    INPUT:
    profile = ['G-CAACA', 
               'GATTACA']
    seq = 'GCATGACA'
    OUTPUT:
    MSA = ['G--CAACA', 
           'G-ATTACA', 
           'GCATGACA']
    """
    # Compatibility 2-sequences and n-sequences
    if isinstance(profile, str):
        profile = [profile]
    # Compute Path
    path = _find_path(profile, seq)

    # Align profile
    MSA = []
    for sequence in profile:
        gen = _generator(sequence)
        MSA.append(''.join([next(gen) if node[1] else '-' for node in path]))
    # Align new sequence
    seq = _generator(seq)
    MSA.append(''.join([next(seq) if node[0] else '-' for node in path]))
    return MSA


if __name__ == "__main__":
    if len(sys.argv) == 1:
        seq1 = "GCAACA"
        seq2 = "GATTACA"
        seq3 = "GCATGACA"
        MSA = needleman_wunsch(seq1, seq2)
        MSA = needleman_wunsch(MSA, seq3)
    elif len(sys.argv) >= 3:
        needleman_wunsch(sys.argv)
    elif sys.argv[1] == "test":
        MSA = needleman_wunsch("ACGTGT", "ACT")
        for s in MSA:
            print(len(s), s)
    elif sys.argv[1] == "1":
        seqs = ['GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTCACCACACTATAAAGTGTTCCTCGCTAAGCTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTATGCTTTCTATGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTCGCCACACTATAAAGTGTTCCTCGCTAAGCTCATA', 'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTCACCACACTATAAAGTGTTCCTCGCTAAACTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTCACCACACTATAAAGTGTTCCTCGCTAAACTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTCACCACACTATAAAGTGTTCCTCGCTAAGCTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTCACCACACTATAAAGTGTTCCTCGCTAAGCTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTCACCACACTATAAAGTGTTCCTCGCTAAGCTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCCTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTTTGATACTCTTGACCTTGTCACCGCACTATAAAGTGTTCCTCGCTAAGCTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCGTACGCCATGGACCGGGAGGTGGCTGCATCGTGCGGAGGCGCGGTCCTTGTGGGTCTGATACTCTTGACCTTGTTACCGCACTATAAAGTGTTCCTCGCCAAGCTCATA',
         'GTGCTGCCTGGTACATCAAGGGCAGGCTGGTCCCTGGGGCGGCGTACGCTTTCTACGGCGTATGGCCGCTGCTCCTGCTCCTGTTGGCGTTGCCACCACGTGCATACGCCATGGACCGGGAGATGGCTGCATCGTGCGGAGGCGCGGTCCTTATCGGTCTGATACTCTTGACCTTGTCTCCACACTATAAAGTGTTCCTCGCTAAGCTCATA']

        article = [0,1,5,3,6,2,4,7,8,9]
        anthony = [9,1,2,4,0,6,7,3,5,8]
        order = article

        MSA = [seqs[order[0]]]
        for i in order[1:]:
            MSA = needleman_wunsch(MSA, seqs[i])
        for s in MSA:
            print(len(s), s)
        print("SCORE", compute_score(MSA))

    elif sys.argv[1] == "2":
        _1 = 'ATGGCGGTCATGGCGCCCCGAACCCTCCTCCTGGTGCTCTCAGGGGTCCTGGCCCTGACCCAGACATGGGCGGGCTCCCACTCCATGAGGTATTTCTACACCTCCATGTCCCGGCCCGGCCGCGGGGAGCCCCGCTTCTTCGCCGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCGCGAGCCAGAGGATGGAGCCGCGGGCGCCGTGGGTGGAGCAGGAGGGGCCGGAGTATTGGGACCGGGAGACACAGAACATGAAGGCCCAGACACAGAATGCCCCAGTGAACCTGCGGAACCTGCGCGGCTACTACAACCAGAGCGAGGCGGGGTCTCACACCCTCCAGACGATGCACGGCTGCGACCTGGGACCCGACGGGCGCCTCCTCCGCGGGTATTACCAGTCCGCCTACGACGGCAAGGATTACTTCGCCCTGAACGAGGACCTGCGCTCCTGGACCGCCGCGGACTTGGCGGCTCAGAACACCCAGCGGAAGTGGGAGGCGGCGGATGTGGCGGAGCAGATTAGAGCCTACCTGGAGGGCCGGTGTGTGGAGTGGCTCCGCAGATACCTGGAGAACGGGAAGGAGACGCTGCAGCGCGCGGACCCCCCCAAGACACATGTGACCCACCACCCCGTCTCTGACCATGAGGCCACCCTGAGGTGCTGGGCCGTGGGCTTCTACCCTGCGGAGATCACACTGACCTGGCAGCGGGATGGGGAGGACCAAACTCAGGACACGGAGCTCATGGAGACCAGGCCTGCAGGAGATGGAACCTTCCAGAAGTGGGCAGCTGTGGTGGTGCCTTCTGGAAAGGAGCAGAGATACACCTGTCATGTGCAGCATGAGGGTCTGCCCAAGCCCCTCACCTTGAGATGGGAGCCGTCTTCCCAGTCCACCATCCCCATCGTGGGCATCATTGCTGGCCTGGTTCTCCTTGGAGCTATGGTCATTGGAGCTGTGGTTGCTGCTGTGATGTGGAGGAGGAAGAGCTCAGATAGAAAAGGAGGGAGCTACTCTCAGGCTGCAAGCAGTGACAGTGCCCAGGGCTCTGATGTGTCTCTCACGGCTTGTAAAGTGTGA'
        _2 = 'ATGGCGGTCATGGCGCCCCGAACCCTCCTCCTGGTGCTCTCAGGGGCCCTGGCCCTGACCCAGACCCGGGCAGGCTCTCACTCCATGAGCTATTTCTACACCTCCATGTCCCGGCCCGGCCGCGGGGAGCCCCGCTTCTTCGCCGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCGCGAGCCAGAGGATGGAGCCGCGGGCGCCGTGGGTGGAGCAGGAGGGTCCAGAGTATTGGGACCGGAGCACACGGATCATGAAGACCGCGACACAGAATGCCCCAGTGGGCCTGCGGAACCTGCGCGGCTACTACAACCAGAGCGAGGCCGGGTCTCACACCTACCAGAGTATGTATGGCTGCGACCTGGGGCCCGACGGGCGCCTCCTCCGCGGGTATTACCAGTCCGCCTACGACGGCAGGGATTACATCGCCCTGAACGAGGACCTGCGCTCCTGGACGGCCGCCGACATGGCGGCTCAGAACACCCAGCGGAAGTGGGAGACGGAAGGTGTGGCAGAGCAGCTGAGCGCCTACCTGGAGGGCGAGTGCCTGGAGTGGCTCCGCAGACACCTGGAGAACGGGAAGGAGATGCTGCAGCGCGCGGACCCCCCCAAGACACATGTGACCCACCACCCCGTCTCTGACCATGAGGCCACCCTGAGGTGCTGGGCCCTGGGCTTCTACCCTGCGGAGATCACACTGACCTGGCAGCGGGATGGAGAGGACCAAACTCAGGACACGGAGCTCGTGGAGACCAGGCCCGCAGGGGATGGAACCTTCCAGAAGTGGGCAGCTGTGGTGGTGCCTTCTGGAAAGGAGCAGAGATACACCTGTCATGTGCAGCATGAGGGTCTGCGTGAGCCCCTCACCCTGAGATGGGAGCCATCTTCCCAGTCCACCATCCCCATCGTGGGCATCATTGCTGGCGTGGTTCTCCTTGGAATTGTGGTCACTGGAGCTGTGATTGCTGCTGTGATATGGAGGAGGAAGAGCTCAGATGGAAAAGGAGGGAGCTACTCTCAGGCTGCAAGCAGTGACAGTGCCCAGGGCTCTGATGTGTCTCTCACGGCTTGTAAAGTGTGA'
        _3 = 'ATGGCGGTCATGGCGCCCCGAACCCTCCTCCTGCTGCTCTCAGGGGCCCTGGCCCTGACCCAGACCTGGGCGAGCTCCCACTCCATGAGGTATTTCTACACCTCCGTGTCCCGGCCCGGCCGCGGGGAGCCCCGCTTCATCGCCGTGGGCTACGTGGACGACACGCAGTTCCTGCGGTTCGACAGCGACGCCGCGAGCCAGAGGCTGGAGCCGCGGGCGCGGTGGGTGGAGCAGGAGGGGCCGGAGTATTGGGACCGGAACACACGGATCGTGAAGGCCGAGACACAGAATGCCCCAGTGAACCTGCAGAACCTGCGCGGCTACTACAACCAGAGCGAGGCCGGGTCTCACACCATCCAGAGGATGTACGGCTGCGACCTGGGGCCCGACGGGCGCCTCCTCCGCGGGTATGAACAGTACGCCTACGACGGCAGGGATTACATCGCCCTGAACGAGGACCTGCGCTCCTGGACCGCCGCGGACATGGCGGCTCAGAACACCCAGCGCAAGTGGGAGGCGGCCCGTGCGGCGGAGCAGCACAGAACCTACCTGGAGGGCGAGTGCCTGGAGTGGCTCCGCAGACACCTGGAGAACGGGAAGGAGACGCTGCAGCGCGCGGACCCCCCCAAGACACATGTGACCCACCACCCCGTCTCTGACTACGAGGCCACCCTGAGGTGCTGGGCCCTGGGCTTCTACCCTGCGGAGATCACACTGACCTGGCAGCGGGATGGAGAGGACCAAACTCAGGACACGGAGCTCGTGGAGACCAGGCCTGCAGGAGATGGAACCTTCCAGAAGTGGGCGGCTGTGGTGGTGCCTTCTGGAAAGGAGCAGAGATACACCTGTCATGTGCAGCATGAGGGTCTGCCCAAGCCCCTCACCTTGAGATGGGAGCCGTCTTCCCAGTCCACCATCGTGGGCATCATTGCTGGCCTGGTTCTCCTTGGAGCTGTGGTCACTGGAGCTGTGGTTGCTGCTGTGATGTGGAGGAGGAAGAGCTCAGATAGAAAAGGAGGAAGCTACTCTCAGGCTGCAAGCAGTGACAGTGCCCAGGGATCTGATGTGTCTCTCACGGCTTGTAAAGTGTGA'
        _4 = 'ATGCGGGTCATGGCGGTCCGAACCCTCCTCCTGCTGCTCTCGGGGGCCCTGGCCCTGACCGAGACCTGGGCCGGCTCCCACTCCATGAGGTATTTCACCACCGCCCTGTCCCGGCCCGGCCGCTGGGAGCCCCGCTTCATCGCCGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCGCGAGTCCGAGGATGGAGCCGCGGGCGCGGTGGATAGAGCAGGAGGGGCCGGAGTATTGGGAGGAGCAGACACGGAGAGCCAAGGGCCACGCACAGACTGACCTAGGGAGCCTGAGGATCCTGCGCGGCTACTACAACCAGAGCGAGGCCGGGTCTCACACCTACCAGTGGATGGCTGGCTGCGACGTGGGACCCGACGGGCGCCTCCTCCGCGGGTATCACCAGCGCGCCTACGACGGCAAGGATTACATCGCCCTGAACGAGGACCTGCGCTCCTGGACCGCCGCGGACGTGGCGGCTCAGAAAACTCAGCGCAAGTGGGAGGCGGCCCGTTTGGCAGAGCAGTGGAGAGCCTACCTGGAGGGCGAGTGCGTGGAGTGGCTCCGCAGATACCTGGAGAACGGGAAGGAGATGCTGCAGCGGACGGACCCCCCAAAGACACACGTGACCCACCACCCCGTCTCTGACCATGAGGCCACCCTGAGGTGCTGGGCCCTGGGCTTCTACCCTGCGGAGATCTCACTGACCTGGCAGCGGGATGGGGAGGACCAAACTCAGGACACTGAGCTTGTGGAGACCAGGCCAGGAGGAGATGGAACCTTCCAGAAGTGGGGAGCTGTGGTGGTGCCTTCTGGAGAAGAGCAGAGATACACGTGCCATGTGCAGCACGAGGGATTGCCGGAGCCCCTCACCCTGAGATGGGAGCCATCTTCCCAGTCCACCATCCCCATCGTGGGCATCGTTGCTGGCCTGGCTGTCCTAGCAGTTGTGGTCATCGGAGCTGTGGTCGCTGCTGTGATGTGGAGGAGGAAGAGCTCAGGTGGAAAAGGAGGGAGCTACTCTCAGGCTGCGTCCAGCGACAGTGCCCAGGGCTCTGATGTGTCTCTCACGGCTTGA'
        _5 = 'ATGCGGTCATGGCTCCCCGAACCCTCCTCCTGCTGCTCTCGGGGGCCCTGGCCCTGACCGAGACCTGGGCCGGCTCGCACTCCATGAAGTATTTCTACACCGCCGTGTCCCGGCCCGGCCGCTGGGAGCCCCACTTCATCTCCGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCGAGAGTCCGAGAAAGGAGCCGCGGGCGCCGTGGGCGGAGCAGGAGGGACCGGAGTATTGGGAAGAGCAGACACGGAGAGCCAAGGCCAACGCACAGGCTGACCGAATGTGCCTGCGGACCGTGCCCGGCTACTACAACCAGAGCGAGGCCGGGTCTCACACCTTCCAGAGTATGTATGGCTGCGACCTGGGGCCCGACTGGCGCCTCCTCCGCGGGTATTACCAGTCCGCCTACGACGGCAGGGATTACATCGCCCTGAACGAGGACCTGCTCTCCTGGACCTCCGCGGACGTGGCGGCTCAGAACACCCAGCGCGAGTGGGAGGCGGACCGTTATGCGGAGCAGCTGAGAGCCTACCTGGAGGGCGAGTGCGTGGAGTCGCTCCGCAGATACCTGGAGAACGGGAAGGAGACGCTGCAGCGCGCGGACCCCCCAAAGACACACGTGACCCACCACCCCATCTCTAACCATGAGGCCACCCTGAGGTGCTGGGCCCTGGGCTTCTACCCTGCGGAGATCACACTGACCTGGCAGCGGGATGGGGAGGACCAAACTCAGGACACAGAGCTTGTGGAGACCAGGCCAGCAGGAGATGGAACCTTCCAGAAGTGGGGAGCTGTGGTGGTGCCTTCTGGAGAAGAGCAGAGATACACGTGCCATGTGCAGCACGAGGGATTGCCAGAGCCCCTCACCCTCAGATGGGAACCATCTTCCCAGTCCACCATCCCCATCGTGGGCATTGTTGCTGGCCTGGCTGTTGTAGCAGTTGTGGTCACCGGAGCTGTGGTCGCTGCTGTGATGTGGAGGAGGAAGAGCTCAGGTGCAAAAGGAGGGAGCTACTCTCAGGCTGCGTCCAACGACAGTGCCCAGGGCTCTGATGTGTCTCTCACGGCTTGA'

        MSA = needleman_wunsch(_1, _3)
        MSA = needleman_wunsch(MSA, _2)
        MSA = needleman_wunsch(MSA, _5)
        MSA = needleman_wunsch(MSA, _4)
        for s in MSA:
            print(len(s), s)
        print(sum([1 for a,b,c,d,e in zip(*MSA) if a==b and b==c and c==d and d==e]))
        print("SCORE", compute_score(MSA))

    elif sys.argv[1] == "3":
        S1='ggcctctgcctaatcacacagatctaacaggattatttc'
        S2='ggcctctgccttataacacaaatcttaacaggactatttc'
        S3='ggcttcagcttatacacaaatcttaaacagggactattc'
        MSA = needleman_wunsch(S1,S2)
        MSA = needleman_wunsch(MSA,S3)
        print(len(MSA[0]), MSA[0])
        print(len(MSA[1]), MSA[1])
        print(len(MSA[-1]), MSA[-1])
        print(sum([1 for a,b,c in zip(*MSA) if a==b and b==c]))
        print("SCORE", compute_score(MSA))
        print("MSA", MSA)

    elif sys.argv[1] == "4":
        Lemur="ATGACTTTGCTGAGTGCTGAGGAGAATGCTCATGTCACCTCTCTGTGGGGCAAGGTGGATGTAGAGAAAGTTGGTGGCGAGGCCTTGGGCAG"
        Gorilla="ATGGTGCACCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGG"
        Mouse="ATGGTTGCACCTGACTGATGCTGAGAAGTCTGCTGTCTCTTGCCTGTGGGCAAAGGTGAACCCCGATGAAGTTGGTGGTGAGGCCCTGGGCAGG"

        MSA = needleman_wunsch(Lemur, Gorilla)
        MSA = needleman_wunsch(MSA, Mouse)
        print(len(MSA[0]), MSA[0])
        print(len(MSA[1]), MSA[1])
        print(len(MSA[-1]), MSA[-1])
        print(sum([1 for a,b,c in zip(*MSA) if a==b and b==c]))
        print("SCORE", compute_score(MSA))
        print("MSA", MSA)
