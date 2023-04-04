import os
class Environement:
    def __init__(self,path_folder,type_parsing):
        type_parsing = type_parsing.lower()
        self.__dico_sequence = self.__parse(path_folder,type_parsing)




    def __parse(self,path_folder,type_parsing):
        """
        Parse all the files
        """
        dico_sequence = {}
        cmpt = 0

        if path_folder[-1] == "/" or path_folder[-1] == "\\": # any one have this problem
            path_folder = path_folder[:-1]

        if type_parsing == "fasta":
            for file in os.listdir(path_folder):
                path_file = path_folder + "/" + file
                dico_sequence[cmpt] = self.__parse_fasta(path_file)
                cmpt += 1


        return dico_sequence
    def __parse_fasta(self,path):
        """
        Parse the fasta file
        """
        sequence = ""
        file = open(path, 'r')
        line =file.readline()
        while line:
            line = file.readline()
            if line :
                if line[-1] == "\n":
                    line = line[:-1]
                sequence += line

        file.close()

        return sequence

