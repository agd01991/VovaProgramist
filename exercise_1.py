from collections import Counter
import re

# Read the input text file
with open('resourse_1.txt', 'r') as file:
    text = file.read()

# Remove punctuation and convert text to lower case
text = re.sub(r'[^\w\s]', '', text).lower()

# Split the text into words
words = text.split()

# Count the frequency of each word
word_counts = Counter(words)

# Sort words by frequency (descending) and lexicographically for ties
sorted_words = sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))

# Write the sorted words and their counts to the output file
with open('result_1.txt', 'w') as file:
    for word, count in sorted_words:
        file.write(f"{word}: {count}\n")

# Optionally print the output to console
for word, count in sorted_words:
    print(f"{word}: {count}")
