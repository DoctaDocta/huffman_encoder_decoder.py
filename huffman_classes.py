#!/usr/bin/env python
# -*- coding: utf-8 -*-t
#huffman_classes.py
top_node = None
outhuff = ''
character_key = [None for x in range(256)]

class TreeNode(object):
    def __init__(self, cnt):
        self.count = cnt

    def __repr__(self):
        return '[{}]{}'.format(self.__class__.__name__,self.count)


    def walk_tree(self, path, switch): #0 at branch, 1 at leaf
                                # store dict in array character_key
        if path is None:
            path = []
        if self.l is not None:
            if isinstance(self.l, Branch):
                self.l.walk_tree(path+[0], switch)
            else:
                str1 = ''.join(str(e) for e in (path+[0]))
                self.l.huffchar = str1
                print '\t',self.l, 'deci:',int(self.l.huffchar,2)
                if switch is 1:
	                character_key[self.l.charac] = self.l.huffchar
        if self.r is not None:
            if isinstance(self.r, Branch):
                self.r.walk_tree(path+[1],switch)
            else:
                str1 = ''.join(str(e) for e in (path+[1]))
                self.r.huffchar = str1
                if switch is 1:
                	character_key[self.r.charac] = self.r.huffchar
                print '\t', self.r, 'deci:', int(self.r.huffchar,2)

	# WE NEED TO PASS THE HUFFMAN CODES in our encoded documents.
	# Serialize (convert to bits) tree using pre-order traversal
    def serialize_preorder(self,output):
        if isinstance(self, Branch):
            output.writebit(1)   # At every branch, output a 1 bit
            print '\tCurrNode is Branch:\twritebit(1), serialize self.left, self.right.'
            self.l.serialize_preorder(output)
            self.r.serialize_preorder(output)  # then the right branch.
        elif isinstance(self, Leaf):
            output.writebit(0)       # At every leaf, output a 0 bit
            str1 = int(self.huffchar, 2)
            output.writebits(str1, 8) # followed by the 8 bitsrepresenting the input symbol on that leaf.
                        #SHOULD I BE WORRIED ABOUT TYPE OF CHARAC I'M PRINGINT???
            print '\tCurrNode is leaf\twritebit(0), writebits(huff,8)\thuff:',self.huffchar,'deci:',str1

	def walk_tree_for_char(self, readbit_cmd): #essentially a tree walk
		if readbit_cmd is 0:
			if isinstance(self.l, Leaf):
				return node_ptr.charac
			else: #we need more bits
				readbit_cmd
				if not readbit_cmd:
					print 'no more bits to read'
					return None
				self.l.walk_tree_for_char(readbit_cmd)
		elif readbit_cmd is 1:
			if isinstance(node_ptr, Leaf):
				return node_ptr.charac #this is the char we print out
			else: #we need more bits!
				readbit_cmd
				if not readbit_cmd:
				    print 'no more bits to read'
				    return None
				self.r.walk_tree_for_char(readbit_cmd)

#subclasses of TreeNode
class Leaf(TreeNode):
    def __init__(self, tup):
        TreeNode.__init__(self, tup[1])
        self.charac = tup[0]
        huffchar = [];

    def __repr__(self):
        return '[{}]{} {}:{}'.format(self.__class__.__name__,self.count,chr(self.charac),self.huffchar)

class Branch(TreeNode):
    def __init__(self,left,right):
        TreeNode.__init__(self, left.count + right.count)
        self.l = left
        self.r = right

    def __repr__(self):
        return '[{}]{}:{}'.format(self.__class__.__name__,self.l,self.r,self.count)
