from pyeda.inter import *


# step 1.  Code in python to convert every number in 0..31 into 5 bit unsigned. Hence,
# each such number gives you an array of 5 bits. example:  3 --->  00011
def convertBinary():
    for i, j in edgeList:
        binaryList.append([int(k) for k in format(i, "05b") + format(j, "05b")])
    
    return binaryList


# step 2. For each edge (i,j) in G (i.e., from node i to node j),  code in python to convert it
# into 10 bits, where the first 5 bits are for the i and the latter 5 bits are for the j.  Notice that the edge
def createEdges():
    for i in range(0, 32):
        for j in range(0, 32):
            if j % 32 == (i + 3) % 32 or j % 32 == (i + 8) % 32:
                edge = (i, j)
                edgeList.append(edge)
    
    return edgeList


# step 3. For each 10-bit array you get in step 2, code in python to convert it into a Boolean formula
def createBooleanExpression():
    for binary in binaryList:
        expression = ""
        index1 = 0
        index2 = 0
        count = 0
        for bit in binary:
            if count < 5:
                if bit == 1:
                    expression += 'x' + str([index1])
                elif bit == 0:
                    expression += '~x' + str([index1])
                if index1 < 5:
                    expression += ' & '
            else:
                if bit == 1:
                    expression += 'y' + str([index2])
                elif bit == 0:
                    expression += '~y' + str([index2])
                if index2 < 4:
                    expression += ' & '
                index2 += 1
            index1 += 1
            count += 1
        expressionList.append(expression)
    
    return expressionList


# step 5 convert into BDD for R, Prime and Even
def createBDD(R, list):
    for expression in list[1:]:
        r = expr(expression)
        rr = expr2bdd(r)
        R = R or rr
    
    return R


# step6 use bdd.compose and bdd.smoothing. To obtain a BDD RR
def BDDCompose(R1, R2):
    for i in range(0, 5):
        R1 = R1.compose(X[i], Z[i])
        R2 = R2.compose(Z[i], Y[i])
    
    RR = R1 and R2
    RR = RR.smoothing(Z)
    return RR


def createPrimeBoolean():
    primeList = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    binaryPrime = []
    
    for prime in primeList:
        binaryPrime.append([int(pr) for pr in format(prime, "05b")])
    
    for primeL in binaryPrime:
        expression = ""
        index = 0
        for prime in primeL:
            if prime == 1:
                expression += 'x' + str([index])
            elif prime == 0:
                expression += '~x' + str([index])
            if index < 4:
                expression += ' & '
            index += 1
        
        booleanPrime.append(expression)
    
    return booleanPrime


def createEvenBoolean():
    evenList = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    binaryEven = []
    
    for even in evenList:
        binaryEven.append([int(e) for e in format(even, "05b")])
    
    for evenL in binaryEven:
        expression = ""
        index = 0
        for even in evenL:
            if even == 1:
                expression += 'x' + str([index])
            elif even == 0:
                expression += '~x' + str([index])
            if index < 4:
                expression += ' & '
            index += 1
        
        booleanEven.append(expression)
    
    return booleanEven


if __name__ == '__main__':
    X = bddvars('x', 5)
    Y = bddvars('y', 5)
    Z = bddvars('z', 5)
    
    # Step 1: create edges
    edgeList = []
    edgeList = createEdges()
    
    # Step 2: Convert Binary
    binaryList = []
    binaryList = convertBinary()
    
    # Step 3: Convert binary to boolean expressions
    expressionList = []
    expressionList = createBooleanExpression()
    
    # step 3': Create boolean expression of prime from 0 - 31
    booleanPrime = []
    booleanPrime = createPrimeBoolean()
    
    # step 3': Create boolean expression of even from 0 - 31
    booleanEven = []
    booleanEven = createEvenBoolean()
    
    # step 4. Create a Boolean formula R over 10 Boolean variables,  x1,...,x5, y1,...,y5
    r = expressionList[0]
    rr = expr(r)
    R = expr2bdd(rr)
    
    # Step 5: Convert expressions into BDD
    RR = createBDD(R, expressionList[1:])
    
    # step 4'. Similarly, you create a Boolean formula P for the set [prime] and a Boolean formula
    # E for the set [even]
    p = booleanPrime[0]
    pp = expr(p)
    Prime = expr2bdd(pp)
    
    # step 5': create BDD for prime expressions
    PP = createBDD(Prime, booleanPrime[1:])
    
    # step 4'. Similarly, you create a Boolean formula P for the set [prime] and a Boolean formula
    # E for the set [even]
    e = booleanEven[0]
    ee = expr(e)
    Even = expr2bdd(ee)
    
    # step 5': create BDD for even expressions
    EE = createBDD(Even, booleanPrime[1:])
    
    # step 7 transitive closure
    while True:
        # step 6: Compose
        H1 = RR
        H2 = H1 or BDDCompose(H1, RR)
        
        if H2.equivalent(H1):
            break
    
    # step 8 decide whether the following is true
    ER = H2 and EE
    JJ = ER.smoothing(Y)
    # negate the result of the smoothing of HH and EE and JJ or not PP
    JP = not (not (JJ or not PP).smoothing(X))
    
    # Check and print the result
    print(f"For each node u in [prime], there is a node v in [even] "
          f"such that u can reach v in even number of steps is {JP}")