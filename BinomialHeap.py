import math
import copy

class BinomialNode:
    def __init__(self, key, value, children, parent):
        self.key = key
        self.value = value
        self.children = children #array
        self.parent = parent #node
        self.height = 0

    def getKey(self):
        return self.key

    def setKey(self, key):
        self.key = key

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getChildren(self):
        return self.children

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def deleteChild(self, child):
        index = self.children.index(child)
        if(index == -1):
            return None
        else:
            node = self.children[index]
            #self.children.pop(index), does this pop empty index or
            self.chlidren[index] = None;
            return node


    def isSame(self, node):#does this need to be recursive, to minimize cases in which nodes have same keys
    #and values? ie check that children & childrens match
        return node.getKey() == self.key and node.getValue() == self.value and node.getParent() == self.parent

    def getParent(self):
        return self.parent

    #wont need to use unless node in between is deleted
    def setParent(self, parent):
        self.parent = parent

    def getHeight(self):
        self.recGetHeight(0, self)
        return self.height

    def recGetHeight(self, counter, node):
        if(node.parent == None):
            self.height = counter
        else:
            self.recGetHeight(counter + 1, node.parent)


    def __repr__(self):
        return "{key: " + str(self.key) + " value: " + str(self.value) +  " }" #" children: " + str(self.children) +


class BinomialTree:
    def __init__(self, key, value):#must have min one node to have tree, make node
        self.root = BinomialNode(key, value, [], None)
        self.degree = 0

    def setRoot(self, root):
        self.root = root

    def getDegree(self):
        return self.degree

    def getRoot(self):
        return self.root

    def upDegree(self):
        self.degree += 1

    def setDegree(self, degree):
        self.degree = degree

    def getSubTrees(self):
        rootChildren = self.root.children
        subTrees = []
        for node in rootChildren:
            newTree = copy.deepcopy(self)
            newTree.root = node
            newTree.setDegree(len(newTree.root.children))
            subTrees.append(newTree)
        return subTrees

    def __repr__(self):
        return self.printPart(self.root,0)

    def recGet(self, key, node):
        if(node.getKey() == key):
            return node
        else:
            for i in node.children:
                if(self.recGet(key, i) == -999):
                    pass
                else:
                    return self.recGet(key, i)
        if(node.children == [] and node.getHeight() == self.degree):
            return None

        return -999

    def printPart(self,node,width):
        if(node==None):
             return "X"

        string=" "
        halfway=math.floor(len(node.getChildren())/2)
        for child in range(0,int(halfway)):
            string+=self.printPart(node.getChildren()[child],width+3)
            string+="\n"+width*" "
        string+=width*" "
        string+=str(node.key)+"\n"
        for child in range(int(halfway), int(len(node.getChildren()))):
            string+=self.printPart(node.getChildren()[child],width+3)
            string+="\n"+width*" "
        return string

class BinomialHeap:
    def __init__(self):
        self.heap = []#array of trees


    def add(self, key, value):
        if(self.heap == []): #checks if it's the very first node
            self.heap.append(BinomialTree(key, value))
        else:
            newBinHeap = BinomialHeap()
            newBinHeap.add(key, value)
            self.merge(newBinHeap)


    def merge(self, binHeap):
        newHeap = []
        iterator = 0
        i = 0
        j = 0
        while(iterator < (len(binHeap.heap) + len(self.heap))):
            if(i == len(binHeap.heap)):
                newHeap.append(self.heap[j])
                j+=1
            elif(j == len(self.heap)):
                newHeap.append(binHeap.heap[i])
                i+=1
            elif(binHeap.heap[i].getDegree() <= self.heap[j].getDegree()):
                newHeap.append(binHeap.heap[i])
                i += 1
            else:
                newHeap.append(self.heap[j])
                j += 1
            iterator += 1
        self.heap = newHeap
        self.clean()


    def clean(self):
        newHeap = []
        i = 0
        j = 1
        while(j < len(self.heap)):
            if(self.heap[i].getDegree() > self.heap[j].getDegree()):
                self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
            if(self.heap[i].getDegree() == self.heap[j].getDegree()):
                self.mergeTrees(self.heap[i], self.heap[j])
                if(self.heap[i].getDegree() < self.heap[j].getDegree()):
                    self.heap.pop(i)
                else:
                    self.heap.pop(j)
                i-=1
                j-=1

            i+=1
            j+=1

    def mergeTrees(self, tree1, tree2):
        if(tree1.root.getKey() < tree2.root.getKey()):
            tree1.root.addChild(tree2.root)
            tree1.upDegree()
            tree2.root.parent = tree1.root
        else:
            tree2.root.addChild(tree1.root)
            tree2.upDegree()
            tree1.root.parent = tree2.root

    def get(self, key):
        i = 0
        while(i < len(self.heap)):
            if(key < self.heap[i].getRoot().getKey()):
                pass
            else:
                val = self.heap[i].recGet(key, self.heap[i].root)
                if(val != None and val != -999):
                    return val
            i+=1
        return None

    def findMin(self):
        roots = []
        rootKeys = []
        for tree in self.heap:
            roots.append(tree.getRoot())
            rootKeys.append(tree.getRoot().getKey())

        minKey = min(rootKeys)
        index = rootKeys.index(minKey)
        return roots[index]

    def findMinTreeIndex(self):
        rootKeys = []
        for tree in self.heap:
            rootKeys.append(tree.getRoot().getKey())

        minKey = min(rootKeys)
        return rootKeys.index(minKey)

    def deleteMin(self):
        minTree = self.heap[self.findMinTreeIndex()]
        subTrees = minTree.getSubTrees()
        newHeap = BinomialHeap()
        for subTree in subTrees:
            newHeap.heap.append(subTree)
        self.heap.pop(self.findMinTreeIndex())
        self.merge(newHeap)


    def bubbleUp(self, node, negInfinity):
        parent = node.parent
        while(parent != None and (negInfinity or node.getKey() < node.parent.getKey())):
            temp = node.key
            node.key = parent.key
            parent.key = temp
            node = parent
            parent = parent.parent

    def delete(self, key):
        if(self.get(key) == None):
            pass
        else:
            node = self.get(key)
            newNode = copy.deepcopy(node)
            self.bubbleUp(node, True)
            self.deleteMin()
            return newNode

    def makeSmall(self):
        self.heap[1].root.children[1].setKey(-10)
        self.bubbleUp(self.heap[1].root.children[1], False)

    def __repr__(self):
        printBoi = ""
        for i in range(len(self.heap)):
            if i != None:
                printBoi += "The tree in the " + str(i) + " slot is:\n"
                printBoi += str(self.heap[i])
                printBoi += '\n'#new line
        return printBoi

def main():
    binHeap = BinomialHeap()
    print("Testing Add:")
    binHeap.add(1, "hi")
    binHeap.add(2, "hel")
    binHeap.add(3, "ther")
    binHeap.add(4, "asdf")
    binHeap.add(5, "asdfasd")
    binHeap.add(7, "asdjfa")
    print("After adding these values, here is the BinomialHeap:")
    print(binHeap)
    print()
    print("Now I can add even more values")
    binHeap.add(15, "asldfj")
    binHeap.add(6, "kjhgf")
    print("And it will restructure completely. Here is the new BinomialHeap:")
    print("While it looks wrong, this is in fact a correct tree of degree 3, with the root of 1 pointing to the 2,3,5")
    print(binHeap)

    print("Now I will test delete:")
    print("Deleting the key 5:")
    print(binHeap.delete(5))
    print(binHeap)
    print("Deleting the key 4:")
    print(binHeap.delete(4))
    print(binHeap)
    print("Now I will try deleting on an empty heap, nothing should happen:")
    binHeap2 = BinomialHeap()
    binHeap2.delete(3)

    print("SEE UNIT TESTING FOR GET")


if __name__ == "__main__":
    main()
