import nltk
from nltk.tokenize import sent_tokenize

# Sample text
text = "I'm writing some sample content. This does not make any sense right now , and will never make sense."


with open('tokens.txt', 'w') as file:
    file.write(text + '\n')

with open('tokens.txt', 'r') as file:
    data= file.readline()
print(sent_tokenize(data))