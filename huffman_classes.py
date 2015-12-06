#!/usr/bin/env python
# -*- coding: utf-8 -*-t
#huffman_classes.py
top_node = None
outhuff = ''
character_key = {}#[None for x in range(256)]
more_bits = 0
huff_key = {}


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
    def printHuff(self):
        print "Leaf[",self.count,",",self.charac,"]"

    def walk_tree(self, path, switch): # 1 at leaf
		self.huffchar = ''.join(str(e) for e in path) #set child.huffchar
		print '\t',self#, 'deci:',self.charac,2) #the deci value is convert to binary by BitWriter
		if switch == 0: character_key[self.charac] = self.huffchar
		if switch == 1: character_key[self.huffchar] = self.charac

	# WE NEED TO PASS THE HUFFMAN CODES in our encoded documents.
	# Serialize (convert to bits) tree using pre-order traversal
    def serialize_preorder(self,output):
        output.writebit(0)       # At every leaf, output a 0 bit
        output.writebits(self.charac, 8) # followed by the 8 bitsrepresenting the input symbol on that leaf.
                    #SHOULD I BE WORRIED ABOUT TYPE OF CHARAC I'M PRINGINT???
        print 'CurrNode is leaf\twritebit(0), writebits(huff,8)\thuff:',self.huffchar,'charac:',self.charac

    def decoder(self, bit, inp, outp, top):
    	print '\t', self.huffchar, '-->', chr(self.charac)
        outp.write(chr(self.charac))
        b = inp.readbit()
        top.decoder(b, inp, outp, top)

class Branch(TreeNode):
    def __init__(self,left,right):
        TreeNode.__init__(self, left.count + right.count)
        self.l = left
        self.r = right

    def __repr__(self):
        return '[{}]{}:{}'.format(self.__class__.__name__,self.l,self.r,self.count)

    def printHuff(self):
        print "Branch[",self.count,','
        self.l.printHuff()
        print ","
        self.r.printHuff()
        print "]"


    def decoder(self, bit, inp, outp, top):
    	if (bit == 0): #--> LEFT CHILD
	    	i = inp.readbit() #we need another bit from file.
    		outchr = self.l.decoder(i, inp, outp, top) #call on LEFT child
    		return outchr
    	elif (bit == 1): # --> RIGHT CHILD
       		i = inp.readbit() #we need another bit from file.
    		outchr = self.r.decoder(i, inp, outp, top) #call decoder from right child
    		return outchr
    	elif (bit is None): #bit is none
    		print 'EOF EOF EOF *******'
    		return None

    def walk_tree(self, path, switch):
        self.l.walk_tree(path+[0],switch)
        self.r.walk_tree(path+[1],switch)

	# Serialize (convert to bits) tree using pre-order traversal
    def serialize_preorder(self, output):
        output.writebit(1)   # At every branch, output a 1 bit
        print 'CurrNode is Branch:\twritebit(1), serialize self.left, self.right.'
        self.l.serialize_preorder(output)
        self.r.serialize_preorder(output)  # then the right branch
