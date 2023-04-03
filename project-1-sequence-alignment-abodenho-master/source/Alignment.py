from source.Matrix import *
from abc import ABC, abstractmethod

class Alignment(ABC):
    def __init__(self, seq1, seq2, I, E, submat, k):
        type = 'a'
        if (I == E):
            type = 'n'
        self.scoreM = ScoreMatrix(seq1,seq2,I,E,submat,type=type)
        self.k = k
        self.lstSolution = []

    @abstractmethod
    def calculate_score(self, i, j):
        """
        Calculate the score of the cell in position i,j in the Score Matrix S, according to the values in S, V and W
        :param i: int, row index
        :param j: int, col index
        :return: float, the score of the cell
        """
        pass

    @abstractmethod
    def backtrack(self, i, j):
        """
        Use the Score Matrices to find the path taken and form the two strings of the alignment
        :param i: int, row index of current position
        :param j: int, col index of current position
        :return: list of tuples of size 5, (str, str, float, (int,int), (int,int)) for seq1 with gaps, seq2 with the
         inserted gaps and score of the alignment and the positions of beginning and end of the alignements sequences
        """
        pass

    def get_solution(self):
        """
        :return: list of tuples of size 5, (str, str, float, (int,int), (int,int)) for seq1 with gaps, seq2 with the
         inserted gaps and score of the alignment and the positions of beginning and end of the alignements sequences
        """

        if len(self.lstSolution) > self.k :
            return self.lstSolution[0:self.k]

        else:
            return self.lstSolution

    def addSolution(self,sol):
        self.lstSolution.append(sol)

    def compute_scores(self, alignment):
        """
        Compute the identity, similarity and number of gaps of an alignment
        :param alignment: list of tuples of size 5, (str, str, float, (int,int), (int,int)) for seq1 with gaps, seq2
        with the inserted gaps and score of the alignment and the positions of beginning and end of the alignments sequences
        :return: list of tuples of 3 floats (rounded two decimal places) respectively ridentity, similarity and gaps ates (in %)
        """

        lst = []
        for elem in alignment:
            seq1 = elem[0]
            seq2 = elem[1]
            lst.append((self.scoreM.calculIdentity(seq1,seq2),self.scoreM.calculSimilarity(seq1,seq2),self.scoreM.calculGap(seq1,seq2)))
        return lst

    @abstractmethod
    def run(self):
        """
        Run the alignment algorithm according to the parameters
        :return:
        """
        pass


class NeedlemanWunsch(Alignment):
    """global"""
    def __init__(self, seq1, seq2, I, E, submat, k):
        """
        Global alignment algorithm
        :param seq1: str, first sequence of amino acids to align
        :param seq2: str, second sequence of amino acids to align
        :param I: float, initial gap value
        :param E: float, extension gap value
        :param submat: SubstitutionMatrix object
        :param k: int, maximum number of solutions to find
        """
        super().__init__(seq1, seq2, I, E, submat, k)
        self.scoreM.setLocal(False)

    def run(self):
        """
        Run the alignment algorithm according to the parameters
        :return:
        """

        self.backtrack(self.scoreM.get_num_rows()-1,self.scoreM.get_num_cols()-1)


    def calculate_score(self, i, j):
        """
        Calculate the score of the cell in position i,j in the Score Matrix S, according to the values in S, V and W
        :param i: int, row index
        :param j: int, col index
        :return: float, the score of the cell
        """

        pass #not use


    def backtrack(self, i, j):
        """
        Use the Score Matrices to find the path taken and form the two strings of the alignment
        :param i: int, row index of current position
        :param j: int, col index of current position
        :return: list of tuples of size 5, (str, str, float, (int,int), (int,int)) for seq1 with gaps, seq2 with the
         inserted gaps and score of the alignment and the positions of beginning and end of the alignements sequences
        """


        resultBacktrack = self.scoreM.backTrack(i, j)

        for pathRep in resultBacktrack :
            seq1,seq2 =self.scoreM.translatePath2Seq(pathRep)
            begin_i,begin_j = pathRep[0]
            self.addSolution((seq1,seq2,self.scoreM.getValue(begin_i,begin_j),pathRep[-1],pathRep[0]))






class SmithWaterman(Alignment):
    """local"""
    def __init__(self, seq1, seq2, I, E, submat, k):
        """
        Local alignment algorithm
        :param seq1: str, first sequence of amino acids to align
        :param seq2: str, second sequence of amino acids to align
        :param I: float, initial gap value
        :param E: float, extension gap value
        :param submat: SubstitutionMatrix object
        :param k: int, maximum number of solutions to find
        """
        super().__init__(seq1, seq2, I, E, submat, k)
        self.scoreM.setLocal(True)
        self.allPointVisited =[]


    def recalculate(self):
        """
        The path taken must be erased (values put to 0 and all the values in the matrix below the last cell of the path
        must be recomputed. The values at 0 must stay at 0.
        :return: None, but the ScoreMatrix S has been modified accordingly
        """

        pass #not use


    def run(self):
        """
        Run the alignment algorithm according to the parameters
        :return:
        """

        sentinelle = self.k
        maxValue = self.getMaxValue()
        while maxValue > 0 and sentinelle > 0:  # il faut au plus k répétition mais on ne prend que les k première
            i, j = self.getMaxPos()
            self.backtrack(i, j)
            maxValue = self.getMaxValue()
            sentinelle -= 1

    def calculate_score(self, i, j):
        """
        Calculate the score of the cell in position i,j in the Score Matrix S, according to the values in S, V and W
        :param i: int, row index
        :param j: int, col index
        :return: float, the score of the cell
        """
        pass #notuse


    def backtrack(self, i, j):
        """
        Use the Score Matrices to find the path taken and form the two strings of the alignment
        :param i: int, row index of current position
        :param j: int, col index of current position
        :return: list of tuples of size 5, (str, str, float, (int,int), (int,int)) for seq1 with gaps, seq2 with the
         inserted gaps and score of the alignment and the positions of beginning and end of the alignements sequences
        """

        resultBacktrack = self.scoreM.backTrack(i, j)
        pathRep = resultBacktrack[0]
        seq1, seq2 = self.scoreM.translatePath2Seq(pathRep)
        begin_i, begin_j = pathRep[0]
        self.addSolution((seq1, seq2, self.scoreM.getValue(begin_i, begin_j), pathRep[-2], pathRep[0]))

        for path in resultBacktrack:
            self.allPointVisited.append(path)

        self.scoreM.recalculate(self.allPointVisited)

    def getMaxValue(self):
        return self.scoreM.get_max()[2]

    def getMaxPos(self):
        return (self.scoreM.get_max()[0],self.scoreM.get_max()[1])

