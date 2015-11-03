#PUFF.PY
# READS AN ENCODED HUFFMAN FILE with a tree in it
#spits back out the original document
import bit_io
from huffman_classes import TreeNode, Branch, Leaf
TreeNode = TreeNode(object)
infile = 'files_to_test_on/testfile.txt.huff'
outfile = infile.split('.')[0]+'.'+infile.split('.')[1]+'.puff'
top_node = None
outhuff = ''


character_key = [False for x in range(256)] # each index from 0-255 corresponds to the char. the val inside is the huffchar
ans = None

def get_huff(car): #enter ord(character) to get back the huffman code.
    print 'printing character_key'
    ans = None
    for x in range(256):
        if (x == car):
            print 'char', chr(x), 'huff', character_key[x]
            ans = character_key[x]
    return ans


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

    #this will read some preliminary lines from the file
    #but we still need to walk the tree, and
    # and read/convert the actual message

print 'reading the infile. First deserializing for the huffcode, then decoding one byte at a time'
with bit_io.BitReader(infile) as input, open(outfile, 'wb') as output:
    top_node = deserialize_preorder(input) #find tree struct
    top_node.walk_tree([],0) #this builds a new tree!
    while True:
        i = input.readbit()
        if i == None: break
        next_char = chr(top_node.walk_tree_for_char(i))
        output.write(next_char)