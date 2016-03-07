from Constants import Constants as C
class EncodeWord(list):
    def __init__(self, ProgramWord,InitialCharacter):
        self.charmap=C.CHARACTER_MAP
        self.ProgramWord=ProgramWord
        self.ListofTupples=[]
        self.DiffTupple=[]
        self.ListofInst=[]
        self.InitialCharacter=InitialCharacter
        self.InitialCharacterTupple=self.getCoordinates(self.InitialCharacter)
        self.StringArray=self.returnStringArray(self.ProgramWord)
        for i in self.StringArray:
            self.ListofTupples.append(self.getCoordinates(i))
        self.getDiff(self.ListofTupples)
        self.getKeyStrokes(self.DiffTupple)
        self.InitialCharacterTupple=self.getCoordinates(i)
        for Inst in self.ListofInst:
            self.append(Inst)
    def returnStringArray(self,ProgramWord):
        self.ProgramWord=ProgramWord.upper()
        return list(self.ProgramWord)

    def getCoordinates(self,Character):
        return self.charmap[Character]
    def getDiff(self,ListofTupples):
        i=0
        for tupple in ListofTupples:
            if i==0:
                diff=(ListofTupples[0][0]-self.InitialCharacterTupple[0],ListofTupples[0][1]-self.InitialCharacterTupple[1])
                self.DiffTupple.append(diff)
            else:
                diff=(ListofTupples[i][0]-ListofTupples[i-1][0],ListofTupples[i][1]-ListofTupples[i-1][1])
                self.DiffTupple.append(diff)
            i= i+1
    def getKeyStrokes(self,DiffTupple):
        for diff in DiffTupple:
            if diff[0]>0:
                for i in range(0,abs(diff[0])):
                    self.ListofInst.append("KEY_DOWN")
            if diff[0]<=0:
                for i in range(0,abs(diff[0])):
                    self.ListofInst.append("KEY_UP")
            if diff[1]>0:
                for i in range(0,abs(diff[1])):
                    self.ListofInst.append("KEY_RIGHT")
            if diff[1]<=0:
                for i in range(0,abs(diff[1])):
                    self.ListofInst.append("KEY_LEFT")
            self.ListofInst.append("KEY_SELECT")
class EncodeTitle(list):
    def __init__(self, ProgramName,InitialCharacter):
        self.ProgramName=ProgramName
        self.InitialCharacter=InitialCharacter
        self.ListofWord=self.ProgramName.split()
        self.InitialCharacter=InitialCharacter
        InteratorWords=0
        self.InstructionSet=[]
        for Word in self.ListofWord:
            if InteratorWords==0:
                for Inst in EncodeWord(Word,self.InitialCharacter):
                    self.InstructionSet.append(Inst)
            else:
                for Inst in EncodeWord(Word,self.ListofWord[InteratorWords-1][-1]):
                    self.InstructionSet.append(Inst)
            InteratorWords=InteratorWords+1
            if InteratorWords<len(self.ListofWord):
                self.InstructionSet.append('KEY_PAUSE')
        for Inst in self.InstructionSet:
            self.append(Inst)

