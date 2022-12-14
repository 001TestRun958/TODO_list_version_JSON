# TODO_list_version_JSON
Flask TODO in python without form

Requirements (all in python 3.10):
- Flask (https://flask.palletsprojects.com/en/2.2.x/installation/#install-flask)
- request
- json
- datetime
- re

To 'get' different data without any change: requests.get('http:///127.0.0.1:5000/..')
- to get a whole todo list: requests.get('http:///127.0.0.1:5000/todos')
- to select tasks which have to be done within a specific period: requests.get('http:///127.0.0.1:5000/todos?date_from=YYYY-mm-dd&date_to=YYYY-mm-dd')
- to select all tasks which should be done until now: requests.get('http:///127.0.0.1:5000/todos?date_to=now')
- to select tasks which should be already done but are not yet: requests.get('http:///127.0.0.1:5000/todos?date_to=now&is_done=False')
- the oldest task which is not finished yet: requests.get('http:///127.0.0.1:5000/most-urgent')

To 'post' a new task: requests.post('http:///127.0.0.1:5000/todo?ukol=ukolNr&body=body&date_to=YYYY-mm-dd')

To 'delete' a task: requests.delete('http:///127.0.0.1:5000/todo/ukolNr')

To sign task as finished or back to in process 'put' : requests.put('http:///127.0.0.1:5000/ukolNr./set-done or set-not-done')

An exception was used to eliminate the FileNotFoundError but as an alternative you can apply os.path.exists()/ os.path.isfile() or see https://stackoverflow.com/questions/1466000/difference-between-modes-a-a-w-w-and-r-in-built-in-open-function.

Except of json, there is still a possibility to process the data as a csv,txt or other file.

The tasks are ordered by their numbers but text (e.g. here ukol1, ukol2, zeppelin1 etc.) was not restricted and has still influence on the order - be aware of it.

The duplicity of tasks/ukol should be excluded.
