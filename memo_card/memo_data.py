from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt 
from random import randint, shuffle


new_question_temp1 = "Нове запитання"
new_answer_temp1 = "Нова відповідь"
text_wrong = "Неправильно"
text_correct = "Правильно"



class Question():
    def __init__(self, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.question = question        
        self.answer = answer        
        self.wrong_answer1 = wrong_answer1        
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3  
        self.is_active = True
        self.attempts = 0
        self.correct = 0
    
    def got_right(self):
        self.correct +=1
        self.attempts +=1
    
    def got_wrong(self):
        self.attempts +=1


class QuestionView():
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.frm_model = frm_model
        self.question = question
        self.answer = answer
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3

    def change(self, frm_model):
        self.frm_model = frm_model

    def show(self):
        self.question.setText(self.frm_model.question)
        self.answer.setText(self.frm_model.answer)
        self.wrong_answer1.setText(self.frm_model.wrong_answer1)
        self.wrong_answer2.setText(self.frm_model.wrong_answer2)
        self.wrong_answer3.setText(self.frm_model.wrong_answer3)

class QuestionEdit(QuestionView):
    def save_question(self):
        self.frm_model.question = self.question.text()
    
    def save_answer(self):
        self.frm_model.answer = self.answer.text()

    def save_wrong(self):
        self.frm_model_answer1 = self.wrong_answer1.text()
        self.frm_model_answer2 = self.wrong_answer2.text()
        self.frm_model_answer3 = self.wrong_answer3.text()

    def set_connects(self):
        self.question.editingFinished.connect(self.save_question)
        self.answer.editingFinished.connect(self.save_answer)
        self.wrong_answer1.editingFinished.connect(self.save_wrong) 
        self.wrong_answer2.editingFinished.connect(self.save_wrong)
        self.wrong_answer3.editingFinished.connect(self.save_wrong)

    def  __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.set_connects()

class AnswerCheck(QuestionView):    
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3, showed_answer, result):
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.showed_answer = showed_answer
        self.result = result      
        
    def check(self):   
        if self.answer.isChecked():   
            self.result.setText(text_correct)    
            self.showed_answer.setText(self.frm_model.answer)    
            self.frm_model.got_right()   
             
        else:      
            self.result.setText(text_wrong)         
            self.showed_answer.setText(self.frm_model.answer)       
            self.frm_model.got_wrong()      

class QuestionListModel(QAbstractListModel):
    ''' у даних знаходиться список об'єктів Question, 
    а також список активних запитань, щоб показати його на екрані '''
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_list = []
    
    def rowCount(self, index):
        ''' кількість елементів для показу: обов'язковий метод для моделі, з якою буде пов'язано віджет "список"'''
        
        return len(self.form_list)

    def data(self, index, role):
            ''' обязательный метод для модели: які дані вона дає по запиту від інтерфейсу'''
            if role == Qt.DisplayRole:
                # передаємо інтерфейсу текст запитання для відображення
                form = self.form_list[index.row()]
                return form.question
    
    def insertRows(self, parent=QModelIndex()):
            ''' цей метод викликається, щоб додати до списку об'єктів нові дані;
            генерується та вставляється одне порожнє запитання'''
            position = len(self.form_list) # вставляємо в кінець, повідомляємо про це наступним рядком
            self.beginInsertRows(parent, position, position) # вставка даних має бути після цього рядка і перед endInsertRows()
            self.form_list.append(Question("Нове запитання", "Правильна відповідь", "Неправильна відповідь", "Неправильна відповідь", "Неправильна відповідь")) # додали нове хапитання до списку даних
            self.insertRows()
            QModelIndex()
            return True


    def removeRows(self, position, parent=QModelIndex()):
            ''' стандартний метод для видалення рядків - після видалення з моделі, рядок автоматично видаляється з екрану'''
            self.beginRemoveRows(parent, position, position) # повідомляємо, що хочемо видалити рядок від position до position 
            self.form_list.pop(position) # видаляємо зі списку елемент з номером position
            self.endRemoveRows() # закінчили видалення (далі бібліотека сама оновлює список на екрані)
            return






def random_AnswerCheck(list_model, w_question, widgets_list, w_showed_answer, w_result):
    '''повертає новий екземпляр класу AnswerCheck, 
    з випадковим запитанням та випадковим розподіленням відповідей по віджетам'''
    frm = list_model.random_question()
    shuffle(widgets_list)
    frm_card = AnswerCheck(frm, w_question, widgets_list[0], widgets_list[1], widgets_list[2], widgets_list[3], w_showed_answer, w_result)
    return frm_card