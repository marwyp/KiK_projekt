from Huffman.Huffman import DynamicHuffmanCode
from Kodowanie_Arytmetyczne.Koder.koder_arytmetyczny import ArithmeticCoder
from Kodowanie_Arytmetyczne.traffic_generator import symbols_generator

arit_encoder = ArithmeticCoder()
print(arit_encoder.coder_adaptive(symbols_generator(10)))
# arit_encoder.coder_adaptive(symbols_generator(10), True))
# arit_encoder.coder_static("abc", True)
# print(arit_encoder.coder_static(symbols_generator(10)))
# print(arit_encoder.coder_static("ggb", True, {"r": 0.4, "g": 0.5, "b": 0.1}))

# Huffman Coding Exampels
huffman = DynamicHuffmanCode(auxiliary_code="ASCII", show_progress=True)
huffman2 = DynamicHuffmanCode(auxiliary_code=None, show_progress=False)

# Example 1
word1 = "aabcdad"
coded_word1 = huffman.coder(word1)
coded_word1_2 = huffman2.coder(word1)

# Example 2
huffman.reset()
word2 = "Ala ma kota"
coded_word2 = huffman.coder(word2)
coded_word2_2 = huffman2.coder(word2)

# results
print("---------Example 1---------\n", word1, ":", coded_word1)
print("", word1, ":", coded_word1_2, "\n")
print("---------Example 2---------\n", word2, ":", coded_word2)
print("", word2, ":", coded_word2_2, "\n")
