huffman_encoder/decoder
NU EECS214 data structures course with github.com/tov/eecs214. This script will be a command line tool that can encode a given file into huffman characters, and is accompanied by a decoding file that can reconstruct the huffman tree and the original file. This algorithm compresses the character byte values by frequency into n-bit length characters. The encoded characters will be nonsensical as interpreted by ascii or a unicode language, so to read the encoded message you must decode it!

## INSTRUCTIONS FOR USE
In mac terminal open the folder containg the pertinent HUFF.PY PUFF.PY HUFFMAN_CLASSES.PY.

You must specify the input file, and an output file (such as input.huff)

[ENCODE A FILE]
$ python huff.py input.txt input.txt.huff

[DECODE A FILE]
$ python puff.py input.huff input.txt.puff

[ENCODE METHOD]
1. Read infile, count frequency of each character.
2. Insert! each (character, frequency) into a Priority Queue. (forest of leaves.)
3. Make a new branch using the characters (trees) with the lightest frequency.
4. Replace those two leaves (char, freqs) with the new branch.
5. Repeat steps 3 and 4 until the Priority queue has one tree. This is the root of the tree.
6. Walk down the tree. That is, at every node, assign a bit value, left children get 1, right children get 0. Now each character will have a bit-length relative to its frequency in the message.
8. Write the length of the encoded message in 32 bits.
7. Serialize the tree. Perform an inorder traversal, for every branch, write a 1 to the outfile. for every leaf, write a 0 and the origin ascii character in 8 bits.
9. Read infile again, for each character write it's encoded counterpart to the outfile.

[DECODE METHOD]
1. Read infile
2. first 32 bits are encoded message length.
3. Deserialize the huffman tree into full use by reverse engineering the sequence of bits.


Object Oriented Binary Search Tree allows us to
