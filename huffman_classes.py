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
	        return '[{}]{} {}:{} (char as int:{})'.format(self.__class__.__name__,self.count,chr(self.charac),self.huffchar, self.charac)
    def walk_tree(self, path, switch): # 1 at leaf
		str1 = ''.join(str(e) for e in path)
		#more_bits = 8 - len(str1) #pad to make huffchar 8 bits. will hold uniqueness
		#str1= str1+ (more_bits * '0')
		self.huffchar = str1 #set child.huffchar
		print '\t',self#, 'deci:',self.charac,2) #the deci value is convert to binary by BitWriter
		if switch == 0: character_key[self.charac] = self.huffchar
		if switch == 1: character_key[self.huffchar] = self.charac
	# WE NEED TO PASS THE HUFFMAN CODES in our encoded documents.
	# Serialize (convert to bits) tree using pre-order traversal
    def serialize_preorder(self,output):
        output.writebit(0)       # At every leaf, output a 0 bit
        output.writebits(self.charac, 8) # followed by the 8 bitsrepresenting the input symbol on that leaf.
                    #SHOULD I BE WORRIED ABOUT TYPE OF CHARAC I'M PRINGINT???
        print '\tCurrNode is leaf\twritebit(0), writebits(huff,8)\thuff:',self.huffchar,'charac:',self.charac

    def decoder(self, inp, path):
    	outchr = chr(self.charac)
    	return outchr

class Branch(TreeNode):
    def __init__(self,left,right):
        TreeNode.__init__(self, left.count + right.count)
        self.l = left
        self.r = right

    def __repr__(self):
        return '[{}]{}:{}'.format(self.__class__.__name__,self.l,self.r,self.count)

    def decoder(self, inp, path):
    	i = inp.readbit() #next bit in file gives us a path
    	if (i == 0):
    		self.l.decoder(inp, path+str(0))
    	elif (i == 1):
    		self.r.decoder(inp, path+str(1))
    	else: #bit is none
    		print 'EOF EOF EOF *******'

    def walk_tree(self, path, switch):
        self.l.walk_tree(path+[0],switch)
        self.r.walk_tree(path+[1],switch)

	# Serialize (convert to bits) tree using pre-order traversal
    def serialize_preorder(self, output):
        output.writebit(1)   # At every branch, output a 1 bit
        print '\tCurrNode is Branch:\twritebit(1), serialize self.left, self.right.'
        self.l.serialize_preorder(output)
        self.r.serialize_preorder(output)  # then the right branch
