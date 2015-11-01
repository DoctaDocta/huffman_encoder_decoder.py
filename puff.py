#PUFF.PY
# READS AN ENCODED HUFFMAN FILE with a tree in it
#spits back out the original document
import bit_io
from huffman_classes import TreeNode, Branch, Leaf
TreeNode = TreeNode(object)
infile = 'testfile.txt.huff'
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
    if bit == None:
        print 'end of file'
    elif bit == 0:
        #read the next 8 bits, they are a character.
        character == reader.readbits(8)
        newLeaf = Leaf((character,0))
        print 'newLeaf', newLeaf
        return newLeaf
    else: #bit == 1:, branch, read the next two bits.
        lchild = deserialize_preorder(reader) #next bit is left child 		-->
        rchild = deserialize_preorder(reader) #next next bit is right child	--> BRANCH
        newBranch = Branch(Leaf((lchild,0)),Leaf((rchild,0))) # deduce huffman code
        print 'newBranch', newBranch
        return newBranch
    #this will read some preliminary lines from the file
    #but we still need to walk the tree, and
    # and read/convert the actual message


with bit_io.BitReader(infile) as input, open(outfile, 'wb') as output:
    while True:
    	top_node = deserialize_preorder(input) #find tree struct
    	top_node.walk_tree([],0) #find huffman code.
        i = input.readbit() #read in actual file
        if not i: break
        print i
        next_char = chr(top_node.walk_tree_for_char(i))
        if next_char is None:
        	break
        else:
	        output.write(next_char)
