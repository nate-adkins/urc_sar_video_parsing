import os
import matplotlib.pyplot as plt
from collections import Counter
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag


def remove_stopwords_and_pos(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    # Remove numbers and single characters
    filtered_words = [word for word in words if word.isalpha() and len(word) > 1]
    # Remove stopwords and certain parts of speech
    filtered_words = [word for word in filtered_words if word.lower() not in stop_words]
    # Remove certain parts of speech (e.g., determiners, prepositions)
    pos_tags = pos_tag(filtered_words)
    filtered_words = [word for word, pos in pos_tags if pos not in ('DT', 'IN')]
    return filtered_words


def count_filtered_words(file_path):
    # Read the content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    # Remove stopwords and certain parts of speech
    return Counter(remove_stopwords_and_pos(text))


def display(list_of_word_freq, num_of_top_words_to_show, num_videos_parsed):
    sorted_freq = sorted(list_of_word_freq, key=lambda x: x[1], reverse=True)

    top_words = sorted_freq[:num_of_top_words_to_show]
    words, frequencies = zip(*top_words)

    plt.figure(figsize=(12, 8))
    bar_width = 0.6  # Adjust the width of the bars
    bars = plt.bar(range(len(words)), frequencies, width=bar_width, tick_label=words, color='skyblue')

    # Add the number inside each bar with vertically centered text
    for bar, freq in zip(bars, frequencies):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, str(freq),
                 fontsize=10, ha='center', va='center', rotation='vertical')

    # Increase font size of text on bars
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Words', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title(f'Top {num_of_top_words_to_show} Words by Frequency in {num_videos_parsed} URC SAR videos', fontsize=16)

    plt.margins(x=0.01)  # Adjust the left and right margins
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin
    plt.show()


def main():
    text_file_directory = "transcript_txt_files/"
    curr_word_freq = Counter()

    num_videos = 0 
    for text_file in os.listdir(text_file_directory):
        text_file_path = os.path.join(text_file_directory, text_file)
        if os.path.isfile(text_file_path):
            curr_word_freq.update(count_filtered_words(text_file_path))
            num_videos += 1 

    display(curr_word_freq.items(), 100, num_videos)

if __name__ == '__main__':
    main()
