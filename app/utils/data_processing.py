"""
Документация модуля
"""

import re
import urllib.parse


def decoder_text(text):
    """
    Документация функции
    """
    start = text.find("[Ответ](") + len("[Ответ](")
    end = text.find(")", start)
    link = text[start:end]
    return urllib.parse.unquote(link)


def parse_answer_file(file_path):
    """
    Документация функции
    """
    with open(file_path, encoding='utf-8') as file:
        lines = file.readlines()

    filtered_lines = ""
    for line_2 in lines:
        if not line_2.strip().startswith(('<div', '[Вернуться к вопросам]', '</div', '\n')) and line_2:
            filtered_lines += line_2
    return ''.join(filtered_lines.strip())


def parse_question_file():
    """
    Парсит файл с вопросами и возвращает список вопросов с их ответами.
    """
    questions = []
    current_question = None
    current_code = []
    file_path = 'app/doc/Список вопросов.txt'
    answer_file_path = "app/doc/"

    with open(file_path, encoding='utf-8') as file:
        for line in file:
            match = re.match(
                r'### (?P<number_question>\d+).\s+(?P<question>.*?)'
                r'\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>',
                line
            )
            if match:
                if current_question:
                    questions.append(current_question)

                question_number_func = int(match.group("number_question"))
                question_text_func = match.group("question")

                decoder_question = decoder_text(line.strip())
                answer_text = parse_answer_file(answer_file_path + decoder_question)

                current_question = [question_number_func, question_text_func, answer_text, None]
                current_code = []

            elif line.startswith("```") and current_question is not None:
                if current_code:
                    current_question[-1] = '\n'.join(current_code) + "\n```"
                    current_code = []
                else:
                    current_code.append(line.rstrip("\n"))
            elif current_code:
                current_code.append(line.rstrip("\n"))

        if current_question:
            if current_code:
                current_question.append('\n'.join(current_code))
            questions.append(current_question)
    return questions
