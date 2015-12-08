#!/usr/bin/env python
# -*- coding: utf-8 -*-t
#huffman_classes.py
top_node = None
character_key = [0 for x in range(256)]#[None for x in range(256)]


class TreeNode(object):
    def __init__(self, cnt):
        self.count = cnt

    def __repr__(self):
        return '[{}]{}'.format(self.__class__.__name__,self.count)

#subclasses of TreeNode
class Leaf(TreeNode):
    def __init__(self, tup):
        TreeNode.__init__(self, tup[1])
        self.charac = tup[0]
        self.huffchar = [];

    def __repr__(self):
    	if self.huffchar and self.charac is None:
	        return '[{}]'.format(self.__class__.__name__)
    	else:
	        return '[{}]{} {}:{}'.format(self.__class__.__name__,self.count,chr(self.charac),self.huffchar)

    def walk_tree(self, path): # 1 at leaf
		self.huffchar = path #set child.huffchar to the path of bits
		print '\t',self#,
		character_key[self.charac] = self.huffchar # add to char key for easy reference

    def buildCwt(self, currentCodeword, table):
        print 'storing', self.charac, 'as codeword', currentCodeword
        table[self.charac] = currentCodeword #Store currentCodeword at index of charcter in table

    # PASS THE HUFFMAN CODES in our encoded documents.
	# Serialize (convert to bits) tree using in-order traversal
    def serialize_preorder(self,output):
        output.writebit(0)       # At every leaf, output a 0 bit
        output.writebits(self.charac, 8) # followed by the 8 bitsrepresenting the input symbol on that leaf.
                    #SHOULD I BE WORRIED ABOUT TYPE OF CHARAC I'M PRINGINT???
        print 'CurrNode is leaf\twritebit(0), writebits(huff,8)\thuff:',self.huffchar,'charac:',self.charac

    def decoder(self, inp, outp, top):
    	print '\t', self.huffchar, '-->', chr(self.charac)
        outp.write(chr(self.charac))

class Branch(TreeNode):
    def __init__(self,left,right):
        TreeNode.__init__(self, left.count + right.count)
        self.l = left
        self.r = right

    def __repr__(self):
        return '[{}]{}:{}'.format(self.__class__.__name__,self.l,self.r,self.count)

    def decoder(self, inp, outp, top):
        i = inp.readbit() #we need another bit from file.
    	if (i == 0): #--> LEFT CHILD
    		outchr = self.l.decoder(inp, outp, top) #call on LEFT child
    		return outchr
    	elif (i == 1): # --> RIGHT CHILD
    		outchr = self.r.decoder(inp, outp, top) #call decoder from right child
    		return outchr

    def walk_tree(self, path):
        self.l.walk_tree(path+[0])
        self.r.walk_tree(path+[1])

    def buildCwt(self, currentCodeword, table):
        self.l.buildCwt(currentCodeword + [0], table)
        self.r.buildCwt( currentCodeword + [1], table)

	# Serialize (convert to bits) tree using in-order traversal
    def serialize_preorder(self, output):
        output.writebit(1)   # At every branch, output a 1 bit
        print 'CurrNode is Branch:\twritebit(1), serialize self.left, self.right.'
        self.l.serialize_preorder(output) #left branch (in order traversal)
        self.r.serialize_preorder(output)  # then the right branch
