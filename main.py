import zipfile

from Huffman.Huffman import DynamicHuffmanCode
from Kodowanie_Arytmetyczne.Koder.koder_arytmetyczny import ArithmeticCoder


with zipfile.ZipFile('cantrbry.zip', 'r') as zip_ref:
    zip_ref.extractall('cantrbry')

with open('cantrbry/alice29.txt', encoding='utf8') as f:
    text = f.read()
f.close()

text_alice = text.upper()
text_alice = text_alice[250:6250]
ala = "Ala ma kota"

# arithmetic coding
arit_encoder = ArithmeticCoder()
tag = arit_encoder.coder_static(text_alice, visualize=True)
print(arit_encoder.dekoder_static(tag))

# Huffman Coding Examples
huffman = DynamicHuffmanCode(auxiliary_code="ASCII", show_progress=True)
huffman2 = DynamicHuffmanCode(auxiliary_code=None, show_progress=False)

huffman_decoder = DynamicHuffmanCode(auxiliary_code="ASCII", show_progress=False)
huffman_decoder_2 = DynamicHuffmanCode(auxiliary_code="ASCII", show_progress=False)

# Example 1
word1 = "aabcdad"
coded_word1 = huffman.coder(word1)
coded_word1_2 = huffman2.coder(word1)
decoded_word = huffman_decoder.decoder(coded_word1)

# Example 2
huffman.reset()
word2 = "Ala ma kota"
coded_word2 = huffman.coder(word2)
coded_word2_2 = huffman2.coder(word2)
decoded_word_2 = huffman_decoder_2.decoder(coded_word2)


# results
print("---------Example 1---------\n", word1, ":", coded_word1)
print("", word1, ":", coded_word1_2, "\n")
print("Decoded: ", decoded_word, "\n")

print("---------Example 2---------\n", word2, ":", coded_word2)
print("", word2, ":", coded_word2_2, "\n")
print("Decoded: ", decoded_word_2, "\n")





