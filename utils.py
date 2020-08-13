from models import *
from contextlib import contextmanager
import messages


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def delete_task(chat_id, task_id, add_to_done=False):
    with session_scope() as session:
        i = 1

        for l in session.query(ToDoList).filter(User.telegram_id == chat_id):
            if l.done:
                continue

            if i == task_id:
                if add_to_done:
                    session.query(ToDoList).filter(ToDoList.id == l.id).update(
                        {ToDoList.done: True}
                    )
                else:
                    session.delete(l)

                return l.description
        i += 1


def get_tasks(chat_id, count=10, done=False):
    with session_scope() as session:
        tasks = ""

        for l in session.query(ToDoList).filter(User.telegram_id == chat_id)[:count]:
            if done and l.done or (not done and not l.done):
                tasks += messages.TASK_LIST_TEMPLATE.format(task=l.description)

        return tasks
