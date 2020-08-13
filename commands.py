from config import bot
from function import *


@bot.message_handler(commands=["start", "help"])
def start(msg):
    with session_scope() as session:
        exist = session.query(User.id).filter_by(telegram_id=msg.chat.id).scalar()

        if not exist:
            session.add(User(name=msg.from_user.first_name, telegram_id=msg.chat.id,),)

    bot.send_message(msg.chat.id, messages.START, parse_mode="HTML")


@bot.message_handler(regexp=r"\/add .+")
def add_task(msg):
    with session_scope() as session:
        user_obj = session.query(User).filter(User.telegram_id == msg.chat.id).first()
        user_obj.todolist.append(ToDoList(description=msg.text.replace("/add ", "")))

    bot.send_message(msg.chat.id, "Added to your list!")


@bot.message_handler(commands=["list"])
def task_list(msg):
    tasks = get_tasks(msg.chat.id, count=50)

    if tasks:
        bot.send_message(msg.chat.id, "In progress:\n" + tasks)
    else:
        bot.send_message(msg.chat.id, "No tasks added. Add first")


@bot.message_handler(regexp=r"\/del \d+")
def del_task(msg):
    bot.send_message(
        msg.chat.id,
        messages.SUCCESSFUL_DELETE.format(
            task=delete_task(msg.chat.id, int(msg.text.split()[1]))
        ),
        parse_mode="HTML",
    )


@bot.message_handler(regexp=r"\/done \d+")
def done_task(msg):
    bot.send_message(
        msg.chat.id,
        messages.ADD_TO_DONE.format(
            task=delete_task(msg.chat.id, int(msg.text.split()[1]), add_to_done=True)
        ),
        parse_mode="HTML",
    )


@bot.message_handler(commands=["history"])
def show_history(msg):
    tasks = get_tasks(msg.chat.id, done=True)

    if tasks:
        bot.send_message(msg.chat.id, "Done:\n" + tasks)
    else:
        bot.send_message(msg.chat.id, "No tasks added. Add first")
