# The functions in this file are to be implemented by students.

from bitio import BitWriter
from bitio import BitReader
import huffman


def read_tree(bitreader):
    '''Read a description of a Huffman tree from the given bit reader,
    and construct and return the tree. When this function returns, the
    bit reader should be ready to read the next bit immediately
    following the tree description.

    Huffman trees are stored in the following format:
      * TreeLeafEndMessage is represented by the two bits 00.
      * TreeLeaf is represented by the two bits 01, followed by 8 bits
          for the symbol at that leaf.
      * TreeBranch is represented by the single bit 1, followed by a
          description of the left subtree and then the right subtree.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.

    Returns:
      A Huffman tree constructed according to the given description.
    '''

    def get_branch(bitreader, tree=None):
        bit = bitreader.readbit()

        if bit == 1:

            left = get_branch(bitreader)
            right = get_branch(bitreader)
            tree = huffman.TreeBranch(left, right)
            return tree

        elif bit == 0:
            bit = bitreader.readbit()

            if bit == 1:
                byte = bitreader.readbits(8)
                leaf = huffman.TreeLeaf(byte)

            elif bit == 0:
                leaf = huffman.TreeLeafEndMessage()

            return leaf

    tree = get_branch(bitreader)

    return tree


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.

    '''
    comp = BitReader(compressed)
    uncomp = BitWriter(uncompressed)

    tree = read_tree(comp)
    while comp.input:

        uncomp_byte = huffman.decode(tree, comp)
        if uncomp_byte == None:
            break

        uncomp.writebits(uncomp_byte, 8)

    uncomp.flush()


def write_tree(tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''
    pass


def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    table = huffman.make_encoding_table(tree)
    uncomp = BitReader(uncompressed)
    comp = BitWriter(compressed)

    write_tree(tree, comp)

    while uncomp.input:
        byte = uncomp.readbits(8)
        comp_byte = table[byte]
        for bit in comp_byte:
            comp.writebit(bit)

    compressed.flush()
