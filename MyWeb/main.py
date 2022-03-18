from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect

from data import db_session
from data.solutions import Solutions

from data.tasks import Tasks
from data.topics import Topics
from data.users import User
from forms.admin import NewTopic, NewTask, NewAns
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def start_index():
    return render_template('start_index.html')


@app.route("/index")
def index():
    db_sess = db_session.create_session()
    topics = db_sess.query(Topics)
    tasks = db_sess.query(Tasks)
    id = 1
    return render_template('index.html',
                           title='Главная страница',
                           topics=topics, tasks=tasks, id=id)


# авторизация пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# #просмотр страницы user
@app.route('/user', methods=['GET', 'POST'])
def user():
    db_sess = db_session.create_session()
    topics = db_sess.query(Solutions)
    tasks = db_sess.query(Tasks)
    a = []
    b = []
    for item in topics:
        if item.user_id == current_user.id:
            a.append(item.id_task)
    for item in tasks:
        if item.id in a:
            b.append(item.content)
    return render_template('user.html',
                           sol=topics, tasks=b)


# регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, email=form.email.data)

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация', form=form)


# заявка на учителя
@app.route('/invite_teach', methods=['GET', 'POST'])
def invite():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.applic = True
    db_sess.commit()
    return redirect('/user')


@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    db_sess = db_session.create_session()
    teach = db_sess.query(User)
    return render_template('admin-2.html',
                           teach=teach)


@app.route('/all-user', methods=['GET', 'POST'])
def allusers():
    db_sess = db_session.create_session()
    teach = db_sess.query(User)
    return render_template('all-user.html',
                           user=teach)


# Принятие учителя
@app.route('/accept_teaching/<int:id>', methods=['GET', 'POST'])
def accept_teaching(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.teach = 1
    user.applic = 0
    db_sess.commit()
    return redirect('/index')


# Принятие учителя
@app.route('/block_user/<int:id>', methods=['GET', 'POST'])
def block_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.block = 1
    db_sess.commit()
    return redirect('/index')


# добавление темы
@app.route('/topic', methods=['GET', 'POST'])
@login_required
def add_topic():
    form = NewTopic()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        topic = Topics()
        topic.name = form.content.data
        db_sess.add(topic)
        db_sess.commit()
        return redirect('/index')
    return render_template('topic.html',
                           title='Добавление темы',
                           form=form)


# показ задач по выбранной теме
@app.route('/show_task/<int:id>', methods=['GET', 'POST'])
def show_task(id):
    db_sess = db_session.create_session()
    topic = db_sess.query(Topics).filter(Topics.id == id).first()
    tasks = db_sess.query(Tasks).filter(Tasks.topic_id == topic.id).all()
    return render_template('show_task.html',
                           title='Просмотр задач по выбранной теме',
                           topic=topic, tasks=tasks)


# добавление задачи
@app.route('/task/<int:id>', methods=['GET', 'POST'])
@login_required
def add_task(id):
    db_sess = db_session.create_session()
    topic = db_sess.query(Topics).filter(Topics.id == id).first()
    form = NewTask()
    if form.validate_on_submit():
        task = Tasks()
        task.topic_id = id
        task.content = form.content.data
        task.ans = form.ans.data
        db_sess.add(task)
        db_sess.commit()
        tasks = db_sess.query(Tasks).filter(Tasks.topic_id == topic.id).all()
        return render_template('show_task.html',
                               title='Просмотр задач по выбранной теме',
                               topic=topic, tasks=tasks)
    return render_template('task.html',
                           title='Добавление задачи',
                           form=form, topic=topic)


# Редактирование текста задачи
@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    form = NewTask()
    if request.method == "GET":
        db_sess = db_session.create_session()
        task = db_sess.query(Tasks).filter(Tasks.id == id).first()
        topic = db_sess.query(Topics).filter(Topics.id == task.topic_id).first()
        if task:
            form.content.data = task.content
            form.ans.data = task.ans
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        task = db_sess.query(Tasks).filter(Tasks.id == id).first()
        if task:
            task.content = form.content.data
            task.ans = form.ans.data
            db_sess.commit()
            topic = db_sess.query(Topics).filter(Topics.id == task.topic_id).first()
            tasks = db_sess.query(Tasks).filter(Tasks.topic_id == topic.id).all()
            return render_template('show_task.html',
                                   title='Просмотр задач по выбранной теме',
                                   topic=topic, tasks=tasks)
    return render_template('task.html',
                           title='Редактирование задачи',
                           form=form, topic=topic)


# просмотр решений задачи
@app.route('/show_ans/<int:id>', methods=['GET', 'POST'])
def show_answer(id):
    db_sess = db_session.create_session()
    answers = db_sess.query(Solutions).filter(Solutions.id_task == id).all()
    task = db_sess.query(Tasks).filter(Tasks.id == id).first()
    problem = task.content
    return render_template('show_ans.html',
                           title='Просмотр решения задачи',
                           answers=answers,
                           problem=problem,
                           id=task.topic_id)


# добавление решения задачи
@app.route('/new_ans/<int:id>', methods=['GET', 'POST'])
@login_required
def add_answer(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Tasks).filter(Tasks.id == id).first()
    problem = task.content
    form = NewAns()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ans = Solutions()
        ans.id_task = id
        ans.content = f'<pre> {form.content.data} </pre>'
        ans.author = current_user.name
        ans.user_id = current_user.id
        db_sess.add(ans)
        db_sess.commit()
        answers = db_sess.query(Solutions).filter(Solutions.id_task == task.id).all()
        return render_template('show_ans.html',
                               title='Просмотр решения задачи',
                               answers=answers,
                               problem=problem,
                               id=task.topic_id)
    return render_template('new_ans.html',
                           title='Добавление решения задачи',
                           form=form,
                           problem=problem,
                           id=task.topic_id)


# редактирование решения задачи
@app.route('/edit_ans/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_answer(id):
    form = NewAns()
    if request.method == "GET":
        db_sess = db_session.create_session()
        ans = db_sess.query(Solutions).filter(Solutions.id == id).first()
        task = db_sess.query(Tasks).filter(Tasks.id == ans.id_task).first()
        if ans:
            form.content.data = ans.content
            form.author.data = ans.author
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        ans = db_sess.query(Solutions).filter(Solutions.id == id).first()
        task = db_sess.query(Tasks).filter(Tasks.id == ans.id_task).first()
        if ans:
            ans.content = form.content.data
            ans.author = form.author.data
            db_sess.commit()
            answers = db_sess.query(Solutions).filter(Solutions.id_task == task.id).all()
        return render_template('show_ans.html',
                               title='Просмотр решения задачи',
                               answers=answers,
                               problem=task.content,
                               id=task.topic_id)
    return render_template('new_ans.html',
                           title='Редактирование решения задачи',
                           form=form,
                           problem=task.content,
                           id=task.topic_id)


# удаление решения задачи
@app.route('/del_ans/<int:id>', methods=['GET', 'POST'])
@login_required
def del_answer(id):
    db_sess = db_session.create_session()
    ans = db_sess.query(Solutions).filter(Solutions.id == id).first()
    id_task = ans.id_task
    db_sess.delete(ans)
    db_sess.commit()
    answers = db_sess.query(Solutions).filter(Solutions.id_task == id_task).all()
    task = db_sess.query(Tasks).filter(Tasks.id == id_task).first()
    problem = task.content
    return render_template('show_ans.html',
                           title='Просмотр решения задачи',
                           answers=answers,
                           problem=problem,
                           id=task.topic_id)


# обработчик адреса
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/index")


def main():
    db_session.global_init("db/tasks.db")
    app.run()


if __name__ == '__main__':
    main()
