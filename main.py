from Huffman.Huffman import DynamicHuffmanCode

#arit_encoder = ArithmeticCoder()
#print(arit_encoder.coder_adaptive(symbols_generator(10)))
# arit_encoder.coder_adaptive(symbols_generator(10), True))
# arit_encoder.coder_static("abc", True)
# print(arit_encoder.coder_static(symbols_generator(10)))
# print(arit_encoder.coder_static("ggb", True, {"r": 0.4, "g": 0.5, "b": 0.1}))

huffman = DynamicHuffmanCode(True)
huffman.coder("aabcdad")
