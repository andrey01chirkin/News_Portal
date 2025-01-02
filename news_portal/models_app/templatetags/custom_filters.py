from django import template

register = template.Library()

@register.filter()
def censor(string):
    bad_words = ["убийство", "фальсификация", "хакеры"]

    if not isinstance(string, str):
        raise ValueError("Фильтр 'censor' можно применять только к строкам.")

    cleaned_string = ''.join(char for char in string if char.isalnum() or char.isspace()) #очистка строки от спец символов (!,$, и т.д.)
    words = cleaned_string.split()

    for word in words:
        if word.lower() in bad_words:
            censored_word = word[0] + "*" * (len(word) - 1)
            string = string.replace(word, censored_word)

    return string
