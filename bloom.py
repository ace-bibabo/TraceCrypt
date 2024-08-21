from bitarray import bitarray
import mmh3
import re


class BloomFilter(object):
    SEEDS = [0, 1, 2]

    # Constructor
    def __init__(self, filter_size):

        self.filter_size = filter_size
        self.bit_array = bitarray(filter_size, endian='little')
        self.bit_array.setall(0)

    # Returns the bits in the bit array
    def __str__(self):
        return self.bit_array.to01()

    # Add the key to the bloom filter
    def add(self, key):
        for seed in self.SEEDS:
            digest = mmh3.hash(key, seed) % self.filter_size
            self.bit_array[digest] = 1

    # Reset all bits to 0
    def reset(self):
        self.bit_array.setall(0)

    # Return a list of positions that are 1 bit.
    def get_DigestPos(self):
        return [i for i, bit in enumerate(self.bit_array) if bit]

    def merge(self, filters_list):
        for dbf in filters_list:
            self.bit_array |= dbf.bit_array

