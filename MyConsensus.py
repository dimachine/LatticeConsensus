# -*- coding: utf-8 -*-
import math
class Context:
    def __init__(self, file_name):
            self.filename=file_name
            cfile=open(file_name)
            self.attr_names=cfile.readline().rstrip().split('\t')
            #rstrip() - удаление пробелов в конце строки
            # split - указание разделителя
            self.objects=[]
            cfile.readline()
            n=0
            for line in cfile:
                sobj=line.rstrip().split('\t')
                obj=[]
                n+=1
                for i in range(len(sobj)):
                    obj.append(int(sobj[i]))
                self.objects.append(obj)
                if n%100==0: print ('Loading ', n)
            cfile.close()
            self.nAttr=len(self.attr_names)
            self.nObj=len(self.objects)

    def objPrime(self, oSet):
        #вычисление оператора штрих от множества объектов
        if oSet==[]:
            return range(self.nAttr)
        aSet=[attr for attr in range(len(self.objects[oSet[0]]))
              if self.objects[oSet[0]][attr]==1]
        aSetC=aSet[:]
        for obj in oSet:
            for attr in aSet:
                if self.objects[obj][attr]==0 and attr in aSetC:
                    aSetC.remove(attr)
                 
        return aSetC
    
    def attrPrime(self,aSet):
        #вычисление оператора штрих от множества признаков
        if aSet==[]:
            return range(self.nObj)
        oSet=[obj for obj in range(len(self.objects)) if self.objects[obj][aSet[0]]==1]
        oSetC=oSet[:]
        #print oSet, aSet
        for attr in aSet:
            for obj in oSet:
                #print obj,attr
                if self.objects[obj][attr]==0 and obj in oSetC:
                    oSetC.remove(obj)
        return oSetC

    def oClosure(self,oSet):
        #вычисление объектного замыкания
        
        return self.attrPrime(self.objPrime(oSet))
    
    def aClosure(self,aSet):
        #вычисление признакового замыкания
        return self.objPrime(self.attrPrime(aSet))


def MyConsensus(context,k):
    p=math.ceil(k/2.00)
    print "p=",p
    O=[g for g in range(context.nObj)]
    S=[]
    g=0
    while len(O)!=0:
        if g in O:
            gprime=context.objPrime([g])
            mprime=context.attrPrime(gprime)
            S.append((mprime,gprime))
            print(mprime)
            O=[x for x in O if x not in mprime]
            print(O)
        g=g+1
    return Process(context, p, S)
    #return S

def Process(context, p, S):
    Cover=[]
    C=S[:]
    S=S[:]
    P=[]
    O=[g for g in range(context.nObj)]
    while len(S)!=0:
        print "S=", S
        (A,B)=S.pop(0)
        print "Length of S", len(S)
        
        print "Extract from S (A,B)=", (A,B)
        print "intersect(A,Cover)=",intersect(A,Cover)
        if len(intersect(A,Cover))==0:
            P.append((A,B))
            Cover=union(Cover,A)
            Rest=substract(O,Cover)
            for g in Rest:
                print "appending (", g,"'',g')"
                X=A[:]
                X.append(g)
                print "X=",X
                Y=context.objPrime(X)
                print "Y=",Y
                if len(Y)>=p:
                    Z=context.attrPrime(Y)
                    print "size is OK (Z,Y)=", (Z,Y)
                    if len([x for x in substract(Z,X) if x<g])==0:
                        print "Canonic generation (Z,Y)=", (Z,Y)
                        P.pop()
                        
                        P.append((Z,Y))
                        print "P=", P
                        Cover=union(Cover,Z)
                    else: print "non-canonic"    
                else: print "non-canonic because of size"
        
        print "We have finished one iteration!"
    print "P=",P,"C=",C  
    if P==C: return P
    print "Starting new Process(context,p,P)"
    return Process(context,p,P)
        
                    



    

def substract(A,B):
    #вычитание множеств
    ret=A[:]
    for b in B:
        if b in A:
            ret.remove(b)
            
    return ret

def intersect(A,B):
    #пересечение множеств
    ret=[]
    for b in B:
        if b in A:
            ret.append(b)
            
    return ret

def isEqual(A,B):
    #провекра на равенство множеств
    for a in A:
        if a not in B:
            return False
    for b in B:
        if b not in A:
            return False
            
    return True

def isLess(A,B):
    #проверка на вложение
    for a in A:
        if a not in B:
            return False
            
    return True

def union(A,B):
    #объединение множеств
    union=[]
    union.extend(A)
    union.extend(B)
    union=list(set(union))
    return union


def ConceptsToPart(Concepts, filename):
    f=open(filename,'w')
    cl={}
    cnt=1
    for C in Concepts:
        for g in C[0]:
            cl[g]=cnt
        cnt+=1
    for key in cl.keys():
        f.write(str(cl[key])+"\n")
        print key,"  ", cl[key]
        
    f.close()    

##
##c=Context('counterex.txt')
##S=MyConsensus(c,3)
##ConceptsToPart(S,"counterexhuy.txt")
##c2=Context('eq.txt')
##S2=MyConsensus(c2,4)
##ConceptsToPart(S2,"eqhuy2.txt")
##c3=Context('noteq.txt')
##S3=MyConsensus(c3,4)
##ConceptsToPart(S3,"noteqhuy3.txt")

c=Context('context.txt')
S=MyConsensus(c,3)
ConceptsToPart(S,"result.txt")

