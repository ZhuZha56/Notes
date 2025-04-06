from PyQt5.QtCore import Qt
import pip
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox
import json

app = QApplication([])



notes_win = QWidget()
notes_win.setWindowTitle('Zаметки')
notes_win.resize(900, 600)



with open("notes_data.json", "r" , encoding='utf-8') as file:
    notes = json.load(file)

list_notes = QListWidget()
list_notes_podskaz = QLabel('Список заметок:')

note_create = QPushButton('Создать заметку') 
note_del = QPushButton('Удалить заметку')
note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
tag_add = QPushButton('Добавить к заметке')
tag_del = QPushButton('Открепить от заметки')
tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_podskaz = QLabel('Список тегов:')

layout_notes = QHBoxLayout()
l_1 = QVBoxLayout()
l_1.addWidget(field_text)

l_2 = QVBoxLayout()
l_2.addWidget(list_notes_podskaz)
l_2.addWidget(list_notes)
r_1 = QHBoxLayout()
r_1.addWidget(note_create)
r_1.addWidget(note_del)
r_2 = QHBoxLayout()
r_2.addWidget(note_save)
l_2.addLayout(r_1)
l_2.addLayout(r_2)

l_2.addWidget(list_tags_podskaz)
l_2.addWidget(list_tags)
l_2.addWidget(field_tag)
r_3 = QHBoxLayout()
r_3.addWidget(tag_add)
r_3.addWidget(tag_del)
r_4 = QHBoxLayout()
r_4.addWidget(tag_search)

l_2.addLayout(r_3)
l_2.addLayout(r_4)

layout_notes.addLayout(l_1, stretch=2)
layout_notes.addLayout(l_2, stretch=1)
notes_win.setLayout(layout_notes)




        
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        save_notes()  



def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        save_notes() 
    else:
        print("Заметка для сохранения не выбрана!")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        save_notes() 
    else:
        print("Заметка для удаления не выбрана!")

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
    else:
        print("Заметка для добавления тега не выбрана!")

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        save_notes()  
    else:
        print("Тег для удаления не выбран!")

def search_tag():
    list_notes_podskaz.setText('Результат поиска:')
    tag = field_tag.text()
    if tag_search.text() == 'Искать заметки по тегу' and tag:
        notest_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notest_filtered[note]=notes[note]
        tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notest_filtered)
    elif tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        tag_search.setText("Искать заметки по тегу")
        list_notes_podskaz.setText('Список заметок:')
    else:
        pass

def save_notes():
    with open("notes_data.json", "w") as file:
        json.dump(notes, file, sort_keys=True)



note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
note_save.clicked.connect(save_note)
note_del.clicked.connect(del_note)
tag_add.clicked.connect(add_tag)
tag_del.clicked.connect(del_tag)
tag_search.clicked.connect(search_tag)


list_notes.addItems(notes.keys())

def confirm_exit(event):
    reply = QMessageBox.question(
        notes_win,
        'Выход',
        'Вы точно хотите выйти?',
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()

notes_win.closeEvent = confirm_exit

notes_win.show()
app.exec_()