"""
This app provides simple flashcards designed to help users prepare for Fachinformatiker exams. 
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import csv
import os

class FlashCards(toga.App):
    def startup(self):
        # Pfad zur CSV-Datei im gleichen Verzeichnis wie app.py
        csv_file_path = os.path.join(os.path.dirname(__file__), 'flashcards.csv')
        self.flashcards = self.load_flashcards(csv_file_path)
        self.current_card_index = 0

        # Hauptbox für die Anordnung der Widgets
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Widgets erstellen
        self.question_label = toga.Label(self.flashcards[self.current_card_index]['question'],
            style=Pack(padding=(0, 5), text_align='center')
        )

        self.answer_label = toga.Label('', style=Pack(padding=(0, 5), text_align='center', visibility='hidden'))

        prev_button = toga.Button('Previous', on_press=self.show_prev_card, style=Pack(padding=5))
        answer_button = toga.Button('Show Answer', on_press=self.show_answer, style=Pack(padding=5))
        next_button = toga.Button('Next', on_press=self.show_next_card, style=Pack(padding=5))

        # Buttons in einer Zeile anordnen
        button_box = toga.Box(style=Pack(direction=ROW, padding=10, alignment='center'))
        button_box.add(prev_button)
        button_box.add(answer_button)
        button_box.add(next_button)

        # Widgets zur Hauptbox hinzufügen
        main_box.add(self.question_label)
        main_box.add(self.answer_label)
        main_box.add(button_box)

        # Hauptfenster erstellen und anzeigen
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def load_flashcards(self, filename):
        flashcards = []
        # Öffne die CSV-Datei mit utf-8-sig Encoding, um das BOM zu entfernen
        with open(filename, encoding='utf-8-sig', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                flashcards.append({'question': row['frage'], 'answer': row['antwort']})
        return flashcards


    def show_prev_card(self, widget):
        self.current_card_index = (self.current_card_index - 1) % len(self.flashcards)
        self.update_card_display()

    def show_next_card(self, widget):
        self.current_card_index = (self.current_card_index + 1) % len(self.flashcards)
        self.update_card_display()

    def show_answer(self, widget):
        self.answer_label.text = self.flashcards[self.current_card_index]['answer']
        self.answer_label.style.visibility = 'visible'

    def update_card_display(self):
        self.question_label.text = self.flashcards[self.current_card_index]['question']
        self.answer_label.text = ''
        self.answer_label.style.visibility = 'hidden'

def main():
    return FlashCards()
