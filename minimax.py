from sys import maxsize #max value

class Node(object):
    def __init__(self,i_depth,i_playerNum,i_sticksRemaining, i_value = 0):
        self.i_depth = i_depth #how deep into the tree (decrease to 0)
        self.i_playerNum = i_playerNum
        self.i_sticksRemaining = i_sticksRemaining
        self.i_Value = i_value #vlue that each node holds (negative infinity, postive inifinity or zeor)
        self.children = []
        self.CreateChildren()

    def CreateChildren(self):
        if self.i_depth >= 0:
            for i in range (1, 3):
                v = self.i_sticksRemaining - i
                self.children.append( Node( self.i_depth -1,-self.i_playerNum,v,self.RealVal(v)))
        
    def RealVal(self, value):
        if value==0:
            return maxsize * self.i_playerNum
        elif value < 0:
            return maxsize * -self.i_playerNum
        return 0

def MiniMax(node, i_depth, i_playerNum):
    if i_depth == 0 or abs(node.i_value) == maxsize:
        return node.i_value
    i_bestValue = maxsize * -i_playerNum

    for i in range(len(node.children)):
        child = node.children[i]
        i_val = MiniMax(child, i_depth - 1, -i_playerNum)
        if abs(maxsize = i_playerNum - i_val) < abs(maxsize*i_playerNum -i_bestValue):
            i_bestValue = i_val

    return i_bestValue

def WinCheck(i_sticks, i_playerNum):
    if i_sticks <= 0:
        print("*"*30)
        if i_playerNum > 0:
            if i_sticks == 0:
                print("You Win")
            else:
                print("Too many, you lose")
        else:
            if i_sticks == 0:
                print("Computer wins")
            else:
                print("Computer error")
        print("*"*30)
        return 0
    return 1

if __name__ == '__main__':
    i_stickTotal = 11
    i_depth = 4
    i_curPlayer = 1
    while i_stickTotal > 0:
        print("\n%d sticks remain. How many would you like to pick up?") %i_stickTotal
        i_choice = input("\n1 or 2: ")
        i_stickTotal -= int(float(i_choice))
        if WinCheck(i_stickTotal, i_curPlayer):
            i_curPlayer *= -1
            
    
        


            
