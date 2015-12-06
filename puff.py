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
outhuff = ''
character = 0
newLeaf = None
newBranch = None

with bit_io.BitReader(infile) as input:
    while True:
        i  = input.readbit()
        print i

'''
#this reads preliminary text in file, the serialized huffman tree.
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


zoinks = True
nodeptr = top_node;
new_huff_char = None;
out_char = None;
print '1. Deserializing for the huffman tree.'
with bit_io.BitReader(infile) as input, open(outfile, 'wb') as output:
    top_node = deserialize_preorder(input) #find tree struct
    print 'Reconstructing the Huffman Tree.'
    top_node.walk_tree([],1)
    print 'Printing char_key',len(character_key), 'entries.','\n',25*'-'
    for x in character_key:
        print '\t\t ',x, chr(character_key[x])
    print 25*'-','\n\n2. Reading encoded file. Decoding...'
    out_char = top_node.decoder(b, input,output, top_node)

    '''