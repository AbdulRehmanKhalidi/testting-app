import Levenshtein


def find_closest_words(input_string, word_list):
    closest_words = []
    for word in word_list:
        distance = Levenshtein.distance(input_string, word)
        if distance <= 1:
            closest_words.append({"suggestion": word, "distance": distance})
    return closest_words