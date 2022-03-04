from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewTopic(FlaskForm):  # Форма добавления темы
    content = StringField("Введите название темы", validators=[DataRequired()])
    submit = SubmitField('Применить')


class NewTask(FlaskForm):  # Форма добавления задачи
    content = TextAreaField("Введите условие задачи",
                            render_kw={'rows': 10},
                            validators=[DataRequired()])
    ans = TextAreaField("Введите ответ",
                        validators=[DataRequired()],
                        render_kw={'rows': 5})
    submit = SubmitField('Применить')


class EditTask(FlaskForm):  # Форма редактирования текста задачи
    content = TextAreaField("Условие задачи",
                            render_kw={'rows': 10},
                            validators=[DataRequired()])
    ans = TextAreaField("Ответ",
                        validators=[DataRequired()],
                        render_kw={'rows': 5})
    submit = SubmitField('Сохранить')


class ShowAns(FlaskForm):  # Удаление решения
    submit = SubmitField('Удалить!')


class ShowTasks(FlaskForm):  # Показ задач по выбранной теме
    submit = SubmitField('Перейти к задачам!')


class NewAns(FlaskForm):  # Форма добавления решения задачи
    content = TextAreaField("Введите решение задачи",
                            render_kw={'rows': 10},
                            validators=[DataRequired()])
    author = StringField('Укажите автора решения')
    submit = SubmitField('Применить')

