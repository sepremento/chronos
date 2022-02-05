import json
import atexit
from datetime import datetime
from pathlib import Path

FILEPATH = Path(__file__).absolute().parent.parent
CUR_MONTH = datetime.today().date().replace(day=1).strftime('%Y-%m')

class ChronoTask:
    def __init__(self, description, tags=None, start_time=None, stop_time=None):
        self._description = description.lower()
        self.set_start_time(start_time)
        self._stop_time = None
        self._tags = self._set_tags(tags)

    def __repr__(self):
        return (f'Task:\nStart time: {self._start_time}\nStop time: '
                f'{self._stop_time}\nDescription: {self._description}\n'
                f'Tags: {self._tags}')

    def set_description(self, description):
        self._description = description.lower()

    def get_description(self):
        return self._description

    def get_tags(self):
        return self._tags

    def add_tag(self, tag):
        if not tag in self._tags:
            self._tags.append(tag.lower())
            return f'Успешно добавили тег: {tag}'
        return f'Такой тег уже есть у задачи: {tag}'

    def remove_tag(self, tag):
        tag = tag.lower()
        if tag in self._tags:
            idx = self._tags.index(tag)
            self._tags.pop(idx)
            return f'Успешно удалили тег: {tag}'
        return f'Нет такого тега: {tag}'

    def set_start_time(self, start_time=None):
        if start_time is None:
            self._start_time = datetime.now().strftime('%x %X')
        else:
            self._start_time = start_time
        return f'Успешно назначили новое время исполнения задачи: {self._start_time}'

    def set_stop_time(self, stop_time=None):
        if stop_time is None:
            self._stop_time = datetime.now().strftime('%x %X')
        else:
            self._stop_time = stop_time
        return f'Успешно назначили новое время завершения задачи: {self._start_time}'

    def to_dict(self):
        return {'Description': self._description,
                'StartTime': self._start_time,
                'StopTime': self._stop_time,
                'Tags': self._tags }

    @classmethod
    def from_dict(cls, d):
        return cls(d['Description'], d['Tags'], d['StartTime'], d['StopTime'])

    def _set_tags(self, tags=None):
        if tags is None:
            return []
        if isinstance(tags, list):
            return list(set([tag.lower() for tag in tags]))
        if isinstance(tags, str):
            return list(set([tag.strip().lower() for tag in tags.split(',')]))


class ChronoLogger:
    def __init__(self):
        if not (FILEPATH / 'data').exists():
            Path.mkdir(FILEPATH / 'data')
        self._buf_path = FILEPATH / 'data/.buf'
        self._log_path = FILEPATH / f'data/{CUR_MONTH}.json'
        self._tasks = self._set_tasks(self._buf_path)
        atexit.register(self._cleanup)

    def __repr__(self):
        if self._tasks:
            return "\n".join([str(task) for task in self._tasks])
        else:
            return "Задач нет!"

    def add_task(self, task):
        if len(self._tasks) < 3:
            self._tasks.append(task)
            return f'Успешно добавили задачу:\n{task}\n'
        return f'Вряд ли ты делаешь больше, чем три дела одновременно'

    def remove_task(self, task_id):
        if isinstance(task_id, str):
            try:
                task_id = int(task_id)
            except ValueError:
                return f'Идентификатор задачи должен быть цифрой'
        if self._tasks:
            try:
                task = self._tasks.pop(task_id)
                return f'Успешно удалили задачу:\n{task}\n'
            except IndexError:
                return f'Не существует задачи с таким индексом: {task_id}'
        return f'Список текущих задач пуст!'

    def get_tasks(self, task_id=None):
        if task_id is None:
            return self._tasks
        if isinstance(task_id, str):
            try:
                task_id = int(task_id)
            except ValueError:
                return f'Идентификатор задачи должен быть цифрой'
        if self._tasks:
            try:
                return self._tasks[task_id]
            except IndexError:
                return f'Не существует задачи с таким индексом: {task_id}'
        return f'Список текущих задач пуст!'

    def finish_task(self, task_id=0):
        if isinstance(task_id, str):
            try:
                task_id = int(task_id)
            except ValueError:
                return f'Идентификатор задачи должен быть цифрой'
        if self._tasks:
            try:
                now = datetime.now().strftime('%x %X')
                task = self._tasks.pop(task_id)
                task.set_stop_time(now)
                task_dict = task.to_dict()
                with open(self._log_path, 'a') as log:
                    log.write(json.dumps(task_dict) + '\n')
                return f'Успешно завершили задачу:\n{task}\n'
            except IndexError:
                return f'Не существует задачи с таким индексом: {task_id}'
        return f'Список текущих задач пуст!'

    def _cleanup(self):
        with open(self._buf_path, 'w') as f:
            f.writelines([json.dumps(task.to_dict()) + '\n' for task in self._tasks])

    def _set_tasks(self, path=None):
        if path is None:
            return []
        with open(path, 'r') as f:
            contents = f.readlines()
            contents = [json.loads(line) for line in contents]
        return [ChronoTask.from_dict(task) for task in contents]

