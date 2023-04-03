import numpy  as np


SPECIALNONE = -6666666

INF = 9999999

############################################################FINIIII #############################################
class Matrix:
    def __init__(self, nrows=0, ncols=0, value=None):
        self.matrice = np.arange(ncols * nrows).reshape(nrows, ncols)
        if value is None:
            value = SPECIALNONE
        self.__setAllValue(value)

    def __getitem__(self, item):
        val = self.getValue(item[0],item[1])
        if val == SPECIALNONE:
            val = None
        return val

    def get_num_cols(self):
        return self.getShape()[1]

    def get_num_rows(self):
        return self.getShape()[0]

    def get_max(self):
        """
        :return: tuple of size 3 of the row index, col index and value of the cell with the maximum value in the matrix
        If several occurences of the maximum value are found, the lowest indices are picked.
        """
        bestValue = (-1,-1,-1000)
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[i])):
                value = self.getValue(i,j)
                if value > bestValue[2]:
                    bestValue = (i,j,value)

        return bestValue

    def set_value(self, i, j, value):
        if self.inMatrice(i, j):
            self.matrice[i][j] = value

    def __setAllValue(self, value):
        """remplace toute les valeurs"""
        for j in range(self.get_num_cols()):
            for i in range(self.get_num_rows()):
                self.set_value(i, j, value)

    #################################### MY METHOD ####################################

    def prettyPrint(self):
        print(self.matrice)

    def getValue(self, ligne, col):
        return self.matrice[ligne][col]

    def inMatrice(self, ligne, col):
        """on vérifie que la ligne et la colonne sont  dans la matrice"""
        rep = True
        maxL = self.matrice.shape[0]
        maxC = self.matrice.shape[1]

        if (col >= maxC or col < 0):
            rep = False

        elif (ligne >= maxL or ligne < 0):
            rep = False

        return rep

    def getShape(self):
        ":returns tuple(Line,Row)"
        return self.matrice.shape

    def getMatrice(self):

        return self.matrice




############################################################FINIIII #############################################
class SubstitutionMatrix(Matrix):
    """
    Format : free
    """

    def __init__(self, file):
        self.taille = 20
        super().__init__(self.taille, self.taille)
        self.path = file
        self.dico = {}  # sert a gardé trace de quel colonne/ligne est quel lettre
        self.parse_file()

    def __getitem__(self, item):
        if item[0].isalpha() and item[1].isalpha():
            return self.compare(item[0],item[1])

        else:
            val = self.getValue(item[0], item[1])
            if val == SPECIALNONE:
                val = None
            return val


    def parse_file(self):
        f = open(self.path, 'r')
        line = ['#']  # cas de base qui s'annule
        numLineMatrix = 0  # ligne de la matrice
        isDicoCreated = False

        while numLineMatrix <= self.taille-1:
            if (line[0] != '#'):  # la ligne contien des information utile
                if (isDicoCreated):
                    self.LineInMatrix(line, numLineMatrix)
                    numLineMatrix += 1

                else:
                    self.createDico(line)
                    isDicoCreated = True

            line = f.readline()

        f.close()

    def createDico(self, line):
        """create a dico using shallowCopy with letter as key and his position for value"""
        pos = 0
        for letter in line:
            if (letter != " " and letter != '\n'):
                if (letter == 'B' or letter == 'Z' or letter == 'X' or letter == '*'):
                    break
                self.dico[letter] = pos
                pos += 1

    def LineInMatrix(self, string, numLine):
        row = 0
        tmp = ""
        for elem in string:
            if (elem != " " and elem != "\n" and not elem.isalpha() and elem != "*"):
                tmp += elem

            else:
                if (len(tmp) != 0):
                    self.set_value(numLine, row, int(tmp))
                    tmp = ""
                    row += 1
        if (len(tmp) != 0):  # cas unique  pour le dernier caractère de fin de matrix (il n'existe pas de "\n" tj)
            self.set_value(numLine, row, int(tmp))

    def compare(self,letter,otherLetter):
        posOne = self.dico[letter]
        posTwo = self.dico[otherLetter]

        return self.getValue(posOne,posTwo)



############################################################  #############################################
## Proposition of implementation, but free for you to use it or not, not included in tests
class ScoreMatrix(Matrix):
    """
    Format : list of list of float values
    """
    def __init__(self, seq1, seq2, I, E, subMatrix, local=False, type = "n"):
        ''' n = pénalité normal / a = pénalatié afine'''
        self.gapExt = - abs(E)
        self.subMatrix = subMatrix
        self.local = local
        self.type = type.lower()
        self.gap = - abs(I)
        self.seqLigne = seq1
        self.seqCol = seq2

        super().__init__(len(self.seqLigne)+1,len(self.seqCol)+1)


        if (self.type == "a" ):
            self.vMatrix = Matrix(len(self.seqLigne)+1,len(self.seqCol)+1)
            self.wMatrix = Matrix(len(self.seqLigne)+1,len(self.seqCol)+1)

        self.run()


    def run(self):
        self.__calculateScore()


    def setLocal(self,bool):
        self.local = bool
        self.run()


    def __calculateScore(self):

        if (self.type == "n"):
            self.__calculateScore_Normal()

        else: #type == "a"
            self.__calculateScore_Affine()

    def setType(self,type):
        self.type = type

    def __getLetterColonne(self,colonne):
        if (colonne == 0):
            raise Exception("not good Colonne for letter")

        return self.seqCol[colonne-1]

    def __getLetterRow(self,ligne):
        if (ligne == 0):
            raise Exception("not good row for letter")
        return self.seqLigne[ligne - 1]

    def __getSubValue(self,ligne,colonne):
        return  self.subMatrix.compare(self.__getLetterRow(ligne), self.__getLetterColonne(colonne))



    def calculSimilarity(self, seq1, seq2):
        """Similarité : nombre d'acides aminés similaires (substitution strictement positive) alignés / longueur alignement"""
        similarity = 0
        for i in range(len(seq1)):
            lettre1 = seq1[i]
            lettre2 = seq2[i]

            if not (lettre1 == '-' or lettre2 == '-'):
                tmp = self.subMatrix.compare(lettre1,lettre2)
                if(tmp > 0):
                    similarity += 1

        rep = similarity/len(seq1)
        rep = round(rep*100,2)


        return rep



    def calculGap(self, seq1, seq2):
        """Gap : nombre de gaps / deux séquences"""
        gap = 0
        taille = 0
        for i in seq1:
            if i == '-':
                gap += 1
            else:
                taille +=1

        for j in seq2:
            if j == '-':
                gap += 1
            else:
                taille +=1

        rep = gap/(taille+gap)
        rep = round(rep*100,2)

        return rep

    def calculIdentity(self, seq1, seq2):
        """Identité : nombre d'acides aminés identiques alignés / longueur alignement"""

        identity = 0

        for i in range(len(seq1)):
            lettre1 = seq1[i]
            lettre2 = seq2[i]

            if lettre1 == lettre2:
                identity +=1

        rep = identity/len(seq1)
        rep = round(rep*100,2)
        return rep

    def reverse(self,seq):
        tmp = ""
        for i in range(1, len(seq)):
            tmp += seq[-i]
        return tmp





    ########################################### TODO BACKTRACK ########################################################################

    def translatePath2Seq(self,path):
        """Translate path into seq with gap
        :return tuple(vertical seq, horizontal seq)"""
        last_i,last_j = path[0][0],path[0][1]
        seqH = ""
        seqV = ""
        for pos in range(0,len(path)):
            actual_i, actual_j = (path[pos][0],path[pos][1])

            delta_i,delta_j = last_i-actual_i,last_j-actual_j

            if (delta_i == 1 and delta_j == 1): #diagonal == match
                seqH += self.__getLetterRow(last_i)
                seqV += self.__getLetterColonne(last_j)
            elif (delta_i == 0 and delta_j == 1): #left == horizontal gap
                seqH += '-'
                seqV += self.__getLetterColonne(last_j)
            else: #delta_i == 1 and delta_j == 0  up == vertical gap
                seqV += '-'
                seqH += self.__getLetterRow(last_i)

            last_i, last_j = actual_i, actual_j

        return (self.reverse(seqH),self.reverse(seqV))

    def erasePath(self, path):
        """met a 0 sur le chemin utilisé"""
        for elem in path:
            i = elem[0]
            j = elem[1]
            self.set_value(i,j,0)
            if(self.type == "a"):
                if (i == 0 and j == 0):
                    pass
                elif (i == 0):
                    self.wMatrix.set_value(i, j, 0)
                elif (j == 0):
                    self.vMatrix.set_value(i, j, 0)



    def backTrack(self,i,j):
        lstRep = []
        path = [(i, j)]
        if self.type == "a":
            self.__backTrackAffin(i,j,path,lstRep)

        else:
            self.__backTrackNormal(i,j,path,lstRep)

        return lstRep



    def __backTrackNormal(self, i, j, path, lstSolution):
        """Backtrack
        :return liste[tuple(i,j)]"""

        lstNextMove = self.__nextPosNormal(i, j,self.getValue(i,j))

        if len(lstNextMove) == 0:
            if not self.local:
                if i == 0 and j == 0:
                    lstSolution.append(path.copy())
            else:
                lstSolution.append(path.copy())
        else:
            for a in lstNextMove:
                Next_i, Next_j = a[0], a[1]  # (i,j)
                path.append(a)
                self.__backTrackNormal(Next_i, Next_j, path, lstSolution)
                path.pop()



    def __backTrackAffin(self,i, j, path, lstSolution):

        lstNextMove = self.__nextPosAffin(i, j, self.getValue(i, j))

        if len(lstNextMove) == 0:
            if not self.local:
                if i == 0 and j == 0:
                    lstSolution.append(path.copy())
            else:
                lstSolution.append(path.copy())
        else:
            for a in lstNextMove:
                Next_i, Next_j = a[0], a[1]  # (i,j)
                path.append(a)
                self.__backTrackAffin(Next_i, Next_j, path, lstSolution)
                path.pop()


    def __nextPosNormal(self,i,j,score):
        """renvoie une liste des next position pour le backtrack cas linéaire"""
        lst = []
        if (self.inMatrice(i - 1, j - 1)):#diago
            if (self.getValue(i-1,j-1)+ self.__getSubValue(i,j) == score):
                lst.append((i-1,j-1))

        if (self.inMatrice(i - 1, j)):#up
            if (self.getValue(i-1,j)+ self.gap == score):
                lst.append((i-1,j))

        if (self.inMatrice(i, j - 1)):#left
            if (self.getValue(i,j-1)+ self.gap == score):
                lst.append((i,j-1))

        return lst


    def __nextPosAffin(self,i,j,score):
        """renvoie une liste des next position pour le backtrack cas affin"""
        lst = []

        if (self.inMatrice(i - 1, j - 1)):  # diago
            if (self.getValue(i - 1, j - 1) + self.__getSubValue(i, j) == score):
                lst.append((i - 1, j - 1))

        if (self.inMatrice(i-1, j)):  # up
            if (self.vMatrix.getValue(i, j) == score):
                lst.append((i - 1, j))

        if (self.inMatrice(i, j - 1)):  # left
            if (self.wMatrix.getValue(i, j) == score):
                lst.append((i, j - 1))

        if(i == 0 and j == 1 ) or (i==1 and j == 0):
            lst.append((0,0))

        if self.local :
            if score == 0:
                return []


        return lst

    def recalculate(self,path):
        allPoint = []
        for elem in path:
            for pos in elem:
                allPoint.append(pos)
        if self.type == "n":
            self.__recalulate_Normal(allPoint)

        else:
            self.__recalulate_Affin(allPoint) #toDELETE



    def __calculateScore_Normal(self):
        maxLigne = self.get_num_rows()
        maxCol = self.get_num_cols()
        for j in range(maxCol):
            for i in range(maxLigne):
                val = self.__getScore_Normal(i, j)
                self.set_value(i, j, val)

    def __getScore_Normal(self,ligne,colonne):
        if (ligne == 0 and colonne >= 0):
            rep = colonne *self.gap
        elif (colonne == 0 and ligne > 0 ):
            rep = ligne *self.gap
        else:
            val1 = self.getValue(ligne-1, colonne) + self.gap
            val2 = self.getValue(ligne, colonne-1) + self.gap
            val3 = self.getValue(ligne-1,colonne-1) + self.__getSubValue(ligne,colonne)

            rep = max(val1,val2,val3)


        if (self.local and rep < 0):
            rep = 0

        return rep

    def __recalulate_Normal(self, path):
        maxLigne = self.get_num_rows()
        maxCol = self.get_num_cols()
        for j in range(maxCol):
            for i in range(maxLigne):
                if (i, j) in path:
                    self.set_value(i, j, 0)
                else:
                    val = self.__getScore_Normal(i, j)
                    self.set_value(i, j, val)


    def __recalulate_Affin(self, path):
        for i in range(self.get_num_rows()):
            for j in range(self.get_num_cols()):
                if (i, j) in path:
                    self.set_value(i, j, 0)
                    self.wMatrix.set_value(i, j, 0)
                    self.vMatrix.set_value(i, j, 0)

                else:
                    val1 = self.__Affine_getScore_V(i, j)
                    val2 = self.__Affine_getScore_W(i, j)
                    if (self.local):
                        if (val1 < 0 and val1 != -INF):
                            val1 = 0
                        if (val2 < 0 and val2 != -INF):
                            val2 = 0

                    self.vMatrix.set_value(i, j, val1)
                    self.wMatrix.set_value(i, j, val2)

                    val3 = self.__Affine_getScore_S(i, j)
                    if (self.local):
                        if (val3 < 0):
                            val3 = 0

                    self.set_value(i, j, val3)



    def __calculateScore_Affine(self):
        maxLigne = self.get_num_rows()
        maxCol = self.get_num_cols()
        for j in range(maxCol):
            for i in range(maxLigne):
                val1 = self.__Affine_getScore_V(i,j)
                val2 = self.__Affine_getScore_W(i,j)
                if(self.local):
                    if(val1<0 and val1 != -INF):
                        val1 = 0
                    if(val2<0 and val2 != -INF):
                        val2= 0

                self.vMatrix.set_value(i,j,val1)
                self.wMatrix.set_value(i,j,val2)

                val3 = self.__Affine_getScore_S(i,j)
                if(self.local):
                    if(val3<0):
                        val3 = 0

                self.set_value(i,j,val3)


    def __Affine_getScore_S(self,i,j):
        if (i==0 and j == 0):
            rep = 0
        elif (i == 0 and j > 0):
            rep = self.gap + (j-1) * self.gapExt
        elif (j == 0 and i > 0):
            rep = self.gap + (i-1) * self.gapExt

        else:
            val1 = self.vMatrix.getValue(i,j)
            val2 = self.wMatrix.getValue(i,j)
            val3 = self.getValue(i - 1, j - 1) + self.__getSubValue(i, j)
            rep = max(val1,val2,val3)

        return rep

    def __Affine_getScore_V(self,i,j):
        if (i == 0 and j == 0):
            rep = -INF
        elif (i == 0 and j > 0):
            rep = -INF
        elif (j == 0 and i > 0):
            rep = 0
        else:
            val1 = self.getValue(i-1,j) + self.gap
            val2 = self.vMatrix.getValue(i-1,j) + self.gapExt
            rep = max(val1,val2)

        return rep

    def __Affine_getScore_W(self,i,j):
        if (i == 0 and j == 0):
            rep = -INF
        elif (i == 0 and j > 0):
            rep = 0
        elif (j == 0 and i > 0):
            rep = -INF

        else:
            val1 = self.getValue(i , j-1) + self.gap
            val2 = self.wMatrix.getValue(i , j-1) + self.gapExt
            rep = max(val1, val2)

        return rep
