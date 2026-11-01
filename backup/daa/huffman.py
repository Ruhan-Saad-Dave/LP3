"""
=============================================================================
Assignment: DAA 2 (Group A)
Title: Write a program to implement Huffman Encoding using a greedy strategy.
Lab: Laboratory Practice - III (BE Computer Engineering - SPPU 2019 Pattern)
=============================================================================
"""

import heapq
from collections import Counter


class HuffmanNode:
    """
    Node representation for Huffman Coding Tree.
    Each node stores character, frequency, and pointers to left and right children.
    """
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Comparator required by heapq for priority queue ordering (Min-Heap based on frequency)
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree_from_frequencies(freq_map):
    """
    Builds the Huffman Tree from a frequency map using a greedy min-heap approach.
    
    Greedy Choice:
        At each step, merge the two nodes having the lowest frequencies.
    
    Time Complexity:  O(n log n) where n is the number of unique characters.
    Space Complexity: O(n) for the priority queue and tree nodes.
    """
    # Step 1: Create leaf nodes for each character and insert into Min-Heap
    min_heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(min_heap)

    # Edge case: single character
    if len(min_heap) == 1:
        root = HuffmanNode(None, min_heap[0].freq)
        root.left = min_heap[0]
        return root

    # Step 2: Merge lowest-frequency pairs until 1 root node remains
    while len(min_heap) > 1:
        # Extract two minimum frequency nodes (Greedy choice)
        left = heapq.heappop(min_heap)
        right = heapq.heappop(min_heap)

        # Create internal node with combined frequency
        parent = HuffmanNode(None, left.freq + right.freq)
        parent.left = left
        parent.right = right

        # Push internal node back into min-heap
        heapq.heappush(min_heap, parent)

    return min_heap[0]


def generate_huffman_codes(node, current_code="", codes=None):
    """
    Traverses the Huffman Tree and assigns variable-length prefix codes:
    Assign '0' for left edge, '1' for right edge.
    """
    if codes is None:
        codes = {}

    if node is None:
        return codes

    # Leaf node: contains an actual character
    if node.char is not None:
        codes[node.char] = current_code if current_code else "0"
        return codes

    generate_huffman_codes(node.left, current_code + "0", codes)
    generate_huffman_codes(node.right, current_code + "1", codes)

    return codes


def encode_string(text, codes):
    """Encodes the original string into a binary sequence."""
    return "".join(codes[char] for char in text)


def decode_string(encoded_text, root):
    """Decodes the binary sequence back to original text using Huffman Tree."""
    decoded_chars = []
    current = root

    for bit in encoded_text:
        current = current.left if bit == "0" else current.right
        if current.char is not None:
            decoded_chars.append(current.char)
            current = root

    return "".join(decoded_chars)


def safe_input(prompt, default_val):
    try:
        val = input(prompt).strip()
        return val if val else default_val
    except (EOFError, KeyboardInterrupt):
        return default_val


def main():
    print("=" * 70)
    print("       DAA Assignment 2: Huffman Encoding (Greedy Strategy)")
    print("=" * 70)

    # Prompt user for input (default matches the manual's example on Page 18: BCAADDDCCACACAC)
    default_text = "BCAADDDCCACACAC"
    print(f"Press ENTER to use Lab Manual example: '{default_text}'")
    user_input = safe_input("Enter text string to encode: ", default_text)
    text = user_input

    print(f"\nTarget String : '{text}'")
    print(f"Total Length  : {len(text)} characters\n")

    # Step 1: Calculate frequencies
    freq_map = Counter(text)

    # Step 2: Build Huffman Tree
    root = build_huffman_tree_from_frequencies(freq_map)

    # Step 3: Generate prefix codes
    codes = generate_huffman_codes(root)

    # Step 4: Display Character Codes Table
    print("-" * 60)
    print(f"{'Character':<12} | {'Frequency':<10} | {'Huffman Code':<15} | {'Length (bits)':<12}")
    print("-" * 60)
    total_encoded_bits = 0
    for char, freq in sorted(freq_map.items(), key=lambda x: (x[1], x[0])):
        code = codes[char]
        char_bits = freq * len(code)
        total_encoded_bits += char_bits
        print(f"{repr(char):<12} | {freq:<10} | {code:<15} | {len(code):<12}")
    print("-" * 60)

    # Step 5: Encode and Decode verification
    encoded = encode_string(text, codes)
    decoded = decode_string(encoded, root)

    print(f"\nOriginal String  : {text}")
    print(f"Encoded Binary   : {encoded}")
    print(f"Decoded String   : {decoded}")
    print(f"Verification     : {'PASSED (Lossless!)' if text == decoded else 'FAILED'}")

    # Step 6: Compression Efficiency Analysis
    original_bits = len(text) * 8  # 8 bits per ASCII character
    compressed_bits = len(encoded)
    saving_percentage = ((original_bits - compressed_bits) / original_bits) * 100

    print("\n" + "=" * 70)
    print("                   COMPRESSION PERFORMANCE")
    print("=" * 70)
    print(f"Original Size (8-bit ASCII) : {original_bits} bits")
    print(f"Compressed Size (Huffman)   : {compressed_bits} bits")
    print(f"Total Storage Saved         : {saving_percentage:.2f}%")
    print("Overall Time Complexity     : O(n log n)")
    print("Auxiliary Space Complexity  : O(n)")
    print("=" * 70)


if __name__ == "__main__":
    main()
