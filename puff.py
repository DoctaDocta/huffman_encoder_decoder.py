#!/usr/bin/env python
#PUFF.PY
# READS A HUFFMAN ENCODED FILE with a tree #writes unencoded message.

from sys import *

if len(argv) != 3:
    stderr.write('Usage: {} INFILE OUTFILE\n'.format(argv[0]))
    exit(2)

import bit_io
from huffman_classes import TreeNode, Branch, Leaf, character_key
TreeNode = TreeNode(object)
infile = argv[1] #'/testfile.txt.huff'
outfile = argv[2] #infile.split('.')[0]+'.'+infile.split('.')[1]+'.puff'

#initializing  vars for functions
top_node = None
outhuff = ''
character = 0
newLeaf = None
newBranch = None

def deserialize_preorder(reader):
    bit = reader.readbit() #read 1 bit.
    if bit == 1: #breanch
        print 'infile',bit,'\tnewBranch'#, newBranch
        lchild = deserialize_preorder(reader) #next bit is left child         -->
        rchild = deserialize_preorder(reader) #next next bit is right child --> BRANCH
        newBranch = Branch(lchild,rchild) # deduce huffman code
        return newBranch
    else: # leaf
        character = reader.readbits(8)
        print 'infile:', bit, '\tnewLeaf','\t', character#, newLeaf
        newLeaf = Leaf((character,0))
        return newLeaf

def match_characters(newhuff, inp):
    if newhuff in character_key:
        out_char = chr(character_key[newhuff])
        return out_char
    else:
        return False

    #this will read some preliminary lines from the file
    #but we still need to walk the tree, and
    # and read/convert the actual message
new_huff_char = None;
out_char = None;
print 'reading the infile. First deserializing for the huffcode, then decoding one byte at a time'
with bit_io.BitReader(infile) as input, open(outfile, 'wb') as output:
    top_node = deserialize_preorder(input) #find tree struct
    print 'Reconstructing the Huffman Tree.'
    top_node.walk_tree([],1) #this faithfully reconstructs the HuffTree! ;)
    print 'Printing char_key',len(character_key), 'entries.','\n',25*'-'
    for x in character_key:
        print '\t\t ',x, character_key[x]
    print 25*'-','\n\nNow reading encoded file...'
    while True:
        #newbit = input.readbit() #one character at a time
        #if newbit == None:
        #    print 'End of encoded message.'
        #    break
        out_char = top_node.decoder(input, '')
        output.write(out_char)
