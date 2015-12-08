#!/usr/bin/env python
#PUFF.PY
# READS A HUFFMAN ENCODED FILE with a tree #writes unencoded message.
from sys import *
import bit_io
from huffman_classes import TreeNode, Branch, Leaf, character_key

if len(argv) != 3:
    stderr.write('Usage: {} INFILE OUTFILE\n'.format(argv[0]))
    exit(2)

#initializing  vars for functions
infile = argv[1] #'/testfile.txt.huff'
outfile = argv[2] #infile.split('.')[0]+'.'+infile.split('.')[1]+'.puff'
TreeNode = TreeNode(object)
top_node = None
character = 0
newLeaf = None
newBranch = None
###########

# reverse engineer the serialized huffman tree --> fully functional huffman tree.
def deserialize_preorder(reader):
    bit = reader.readbit() #read 1 bit.
    if bit == 1: #breanch
        print 'infile',bit,'\tnewBranch'#, newBranch
        lchild = deserialize_preorder(reader) #next bit is left child #preorder
        rchild = deserialize_preorder(reader) #next next bit is right child
        newBranch = Branch(lchild,rchild) # deduce huffman code
        return newBranch
    else: # leaf
        character = reader.readbits(8)
        print 'infile:', bit, '\tnewLeaf','\t', chr(character)#, newLeaf
        newLeaf = Leaf((character,0))
        return newLeaf


huff_length = None;
print 'Deserializing for the huffman tree.'
with bit_io.BitReader(infile) as input, open(outfile, 'wb') as output:
    huff_length = input.readbits(32) #read first 32 bits for byte-size of encoded message
    print "size of encoded file", huff_length
    top_node = deserialize_preorder(input) #remake huffman tree.
    #top_node.walk_tree([]) #
    print 'Reconstructing the Huffman Tree.'
    print 25*'-','\n\nReading encoded file. Decoding...'
    for x in range(0,huff_length): #only walk tree for specified number of bits.
        top_node.decoder(input,output, top_node)