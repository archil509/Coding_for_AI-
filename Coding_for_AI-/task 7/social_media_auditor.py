    # task 1
word_counts = {}

text = """The quick brown fox jumps over the lazy dog. The dog barks, 
and the fox runs away. The quick brown fox is quick and clever."""

for word in text.split():
    word_counts.setdefault(word, 0)
    word_counts[word] += 1

print("Word Frequency Counter Results:")
print("-" * 35)
for word, count in sorted(word_counts.items()):
    print(f"{word:15} : {count}")


    # task2
    
import string
text = "AI is powerful. AI, is easy to learn! ai is useful ---"
word_counts = {}

for raw_word in text.split():
    cleaned_word = raw_word.lower().strip(string.punctuation)
    if not cleaned_word:
        continue

    word_counts.setdefault(cleaned_word, 0)
    word_counts[cleaned_word] += 1

print(word_counts)

#task3

platform_a_followers = ["krupal", "harsh", "vikas", "Neha"]
platform_b_followers = ["Priya", "Neha", "virat", "harsh"]
set_a = set(platform_a_followers)
set_b = set(platform_b_followers)
both_platforms = set_a & set_b
only_a = set_a - set_b
only_b = set_b - set_a
print("Both platforms:", both_platforms)
print("Only Platform A:", only_a)
print("Only Platform B:", only_b)
