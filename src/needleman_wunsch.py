import numpy as np
import sys

""" Similarity matrix
    A   G   C   T
A    1  -1  -1  -1
G   -1   1  -1  -1
C   -1  -1   1  -1
T   -1  -1  -1   1
"""

score = {'match': 2, 'mismatch': -1, 'gap':-2}

def _generator(string):
    for s in string:
        yield s

def _aligned_score(aligned_char, char):
    return sum([score['match'] if c==char else score['mismatch'] for c in aligned_char])


def _compute_matrix(aligned_seqs, new_seq):
    # Init score matrix (cumulative gap penality for first row and column, else 0)
    matrix = [[(a+b)*score['gap'] if a==0 or b==0 else 0 for b in range(1+len(new_seq))] for a in range(1+len(aligned_seqs[0]))]
    # Init direction matrix to keep track of the best direction
    directions = [[(0,0) for b in range(1+len(new_seq))] for a in range(1+len(aligned_seqs[0]))]

    # Fill the matrices
    for i, aligned_char in enumerate(zip(*aligned_seqs)):
        for j, char in enumerate(new_seq):
            s = [((0,-1), matrix[i][j+1] + score['gap']), # from top
                ((-1,0), matrix[i+1][j] + score['gap']), # from left
                ((-1,-1), matrix[i][j] + _aligned_score(aligned_char, char))] # from top-left
            best = max(s, key=lambda x: x[1])
            matrix[i+1][j+1] = best[1]
            directions[i+1][j+1] = best[0]
    return directions

def _find_path(aligned_seqs, new_seq):
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

def needleman_wunsch(seq1, seq2):
    path = _find_path([seq1], seq2)
    seq1 = _generator(seq1)
    seq2 = _generator(seq2)

    res1 = []
    res2 = []
    for node in path:
        res1.append(next(seq1) if node[1] else '-')
        res2.append(next(seq2) if node[0] else '-')

    print(''.join(res1))
    print(''.join(res2))
    return ''.join(res1), ''.join(res2)

def needleman_wunsch_multiple(aligned_seqs, seq):
    path = _find_path(aligned_seqs, seq)
    seq = _generator(seq)

    res = []
    for node in path:
        res.append(next(seq) if node[0] else '-')

    print(''.join(res))
    return ''.join(res)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        needleman_wunsch(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 3:
        needleman_wunsch_multiple(sys.argv[1:-1], sys.argv[-1])
    else:
        seq1 = 'GAAAAAAT' #'GATTACA'
        seq2 = 'GAAT'#'GCATGCG'
        a,b = needleman_wunsch(seq1, seq2)
