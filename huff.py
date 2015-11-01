#!/usr/bin/env python
# -*- coding: utf-8 -*-t
#huff.py

import bit_io
from huffman_classes import TreeNode, Branch, Leaf, character_key
TreeNode = TreeNode(object)

infile = 'files_to_test_on/testfile.txt'
outfile = infile+'.huff'

frequency_table = [0 for x in range(256)]
ans = None
#once we have out tree, we make a dictionary so it is easy to encode.
#input a char --> huffchar
def char_to_huff(car): #enter ord(character) to get back the huffman code.
    #print 'printing character_key'
    ans = None
    for x in range(256):
        if (x == car):
            print '\t ascii:',chr(x),'huff:',character_key[x],'\tdeci:',int(character_key[x],2)
            ans = character_key[x]
    return ans

#MAKE HUFFMAN TREE FROM FREQUENCY TABLE.
queue = []
def make_huffman_tree(tabla):
    #convert frequency table into leaves
    if tabla:
        for x in range(256):
            if (tabla[x] !=0):
                newLeaf = Leaf((x, tabla[x]))
                queue.append(newLeaf) #add it to our queue.
        print 'Number of initial tree nodes from freq table:', len(queue)
    else:
        print "Can't find the frequency table!"
        return False
    print 'Making table out of tree nodes...'
    queue.sort(key=lambda x: x.count, reverse=True)
    while (len(queue) > 1):
        queue.sort(key=lambda x: x.count, reverse=True)
        l, r = queue.pop(), queue.pop()
        node = Branch(l,r)
        queue.append(node)
        #print  l, r,'replaced with', node
    return queue.pop()


#READ THE INFILE
# make Frequency table and huffman tree and character_key
with open(infile, "rb") as input:
    while True:
        b = input.read(1)
        if not b: break
        #print 'char',b,'ord(char)', ord(b)
        frequency_table[ord(b)] += 1 #increment that index of freq table

#using the functions above to make a tree
top_node = make_huffman_tree(frequency_table)
if top_node == False:
    print 'ERROR ****'
    pass
print 'Binary Search Tree built.\nWalking down from top node; printing huffman code.'
top_node.walk_tree([],1)


#TRANSCRIBING THE INFILE TO AN OUTFILE
#READ THE INFILE
print '\nbit_io.BitWriter uses decimal equivalent of huffchar to write multiples bits.'
print '\nNow encoding the outfile.'
huff = []
switch = 0
with open(infile, "rb") as input, bit_io.BitWriter(outfile) as output:
    while True:
        switch+=1
        if switch is 1:
            print '\n 1. Serialize huffman code using preorder traversal from top node.'
            top_node.serialize_preorder(output)# called once
            print '\n 2. Encode message using huffman'
        b = input.read(1)
        if not b: break
        b = ord(b)
        print '\n\tinfile char:',b
        huff = int(char_to_huff(b),2)
        output.writebits(huff, 8)
print '\n'
print 'reading the outfile one bit at a time'
with bit_io.BitReader(outfile) as input:
    while True:
        b = input.readbit()
        if not b: break
        print 'outfile:',b