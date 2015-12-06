#!/usr/bin/env python
# -*- coding: utf-8 -*-t
#huff.py
from sys import *

if len(argv) != 3:
    stderr.write('Usage: {} INFILE OUTFILE\n'.format(argv[0]))
    exit(2)

import bit_io
from huffman_classes import TreeNode, Branch, Leaf, character_key, huff_key

TreeNode = TreeNode(object)

infile = argv[1] #'files_to_test_on/testfile.txt'
outfile = argv[2] #infile+'.huff'

frequency_table = [0 for x in range(256)]
ans = None
#once we have out tree, we make a table so it is easy to lookup.
#input a char --> huffchar
def char_to_huff(car): #enter ord(character) to get back the huffman code.
    #print 'printing character_key'
    for x in range(256):
        if x == car:
            ans = character_key[x]
    print '\t\t\tchar:',chr(car),'huff:',ans,' huff int:',int(ans,2)
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
    return queue.pop()

#READ THE INFILE
# make Frequency table by tallying characters
with open(infile, "rb") as input:
    while True:
        b = input.read(1)
        if not b:
            break
        print b
        frequency_table[ord(b)] += 1 #increment that index of freq table

top_node = make_huffman_tree(frequency_table)
if top_node == False:
    print 'ERROR ****'
    pass

print 'Binary Search Tree built.\nWalking down from top node; printing huffman code.'
top_node.walk_tree([],0)
huff = False
switch = 0


#TRANSCRIBING THE INFILE TO AN OUTFILE
#READ THE INFILE
print '\nbit_io.BitWriter uses decimal equivalent of huffchar to write multiples bits.'
print '\nNow encoding the outfile.'

top_node.printHuff()


# SERIALIZE THE HUFFMAN TREE, WRITE OUT THE SEQUENCY OF BITS TO HUFF (output) FILE
with bit_io.BitWriter(outfile) as output:
    print '\n 1. Serializes huffman code using preorder traversal from top node.'
    top_node.serialize_preorder(output)# called once
    print '\n 2. Encode message using huffman key'
    print 'Character_key has', len(character_key), 'entries.'
    print 'char\thuffchar'
    for x in character_key:
        print chr(x),'\t',character_key[x]
    print'\nEncoding file'

converted_huff = None # initialize variable for encoder.

#READ IN MESSAGE, ENCODE BITS USING HUFFMAN, WRITE OUTPUT TO HUFF FILE
with open(infile, "rb") as input,bit_io.BitWriter(outfile) as output:
    while True:
        b = input.read(1)
        if not b:
            break
        #convert bit, b, to huff chars
        converted_huff = character_key[ord(b)];
        for x in converted_huff:
            output.writebit(x)
        #use bitwriter
        print b, "-->", converted_huff


