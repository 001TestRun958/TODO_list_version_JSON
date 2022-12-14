from flask import Flask, request
from datetime import datetime
import json
import re
import os
    
my_app = Flask('my_server')

class DB:

    DATA_FILE='data.json'

    # to order ukol e.g. ukol1, ukol2 etc.
    def natural_sort(self,l): 
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(l, key=alphanum_key)

    def change_data(self,data):
        keys=self.natural_sort(data.keys())
        data={x:data[x] for x in keys}
        return data

    # to open data.json file
    def open_json(self):
        with open(self.DATA_FILE, 'r') as data_file:
            data=json.load(data_file)
            return data

    # to change DATA_FILE file
    def overwrite_json(self,data):
        data.update(data)
        with open(self.DATA_FILE,"w", encoding='utf-8') as data_file:
            json.dump(data,data_file,indent=4)
            return data

    # for work with string like a datetime datatype
    def date_to_status(self,date):
        return datetime(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))

    def today(self):
        today=str(datetime.now())
        date_to=today.split(' ')[0]
        return date_to

db=DB()


# to sign task as finished or back to in process: requests.put('http:///127.0.0.1:5000/ukolNr./set-done or set-not-done')
@my_app.route('/<put_ukol>/<put_params>', methods=['PUT'])
def put_set_done(put_ukol,put_params):
    # %s for string, %d for integer, %f for float
    
    try:
        data=db.open_json()
    except FileNotFoundError:
        return f'No file yet',404
    else:
        if put_ukol not in data:
            return 'No data for %s' % put_ukol,400
        else: 
            if put_params=='set-done':
                data[put_ukol]['is_done']='True'
            elif put_params=='set-not-done':
                data[put_ukol]['is_done']='False'
            else:
                return 'No data for %s :' % put_ukol+ data[put_ukol]['is_done'],400
        data=db.change_data(data)
        db.overwrite_json(data)
        print(data)
        return 'ok'

# to get different data without any change: requests.get('http:///127.0.0.1:5000/..')
@my_app.route("/todos")
def todos():

    date_from=request.args.get('date_from')
    date_to=request.args.get('date_to')
    is_done=request.args.get('is_done')

    try:
        data=db.open_json()
    except FileNotFoundError:
        return "No data",404
    else:
        # to get a whole todo list: requests.get('http:///127.0.0.1:5000/todos')
        if  date_from == None and date_to == None and date_to != 'now': 
            data=db.change_data(data)
            print(data)
            return 'ok'
        # to select tasks which have to be done within a specific period: requests.get('http:///127.0.0.1:5000/todos?date_from=YYYY-mm-dd&date_to=YYYY-mm-dd')    
        elif date_from != None and date_to != None and date_to != 'now':
            date_from=db.date_to_status(date_from)
            date_to=db.date_to_status(date_to)
            data={key:value for key, value in data.items() if (date_from<=db.date_to_status(value['date_to'])) and (db.date_to_status(value['date_to'])<=date_to)}
            data=db.change_data(data)
            print(data)
            return 'ok'
        # to select tasks which should be already done but are not yet: requests.get('http:///127.0.0.1:5000/todos?date_to=now&is_done=False')    
        elif date_to=='now' and is_done=='False':
            data={key:value for key, value in data.items() if value['is_done']=='False' and (db.date_to_status(value['date_to'])<=db.date_to_status(db.today()))}
            data=db.change_data(data)
            print(data)
            return 'ok'
        # to select all tasks which should be done until now: requests.get('http:///127.0.0.1:5000/todos?date_to=now')    
        elif date_to=='now':
            data={key:value for key, value in data.items() if db.date_to_status(value['date_to'])<=db.date_to_status(db.today())}
            data=db.change_data(data)
            print(data)
            return 'ok'
        else:
            return 'No valid request',404

# the oldest task which is not finished yet: requests.get('http:///127.0.0.1:5000/most-urgent')
@my_app.route('/<urgent>')
def urgent(urgent):
    try:
        data=db.open_json()
    except FileNotFoundError:
        return "No data",404
    else:
        if urgent=='most-urgent':
            not_done_list={key:value for key,value in data.items() if value['is_done']=='False'}
            list_string_dates=[(value['date_to']) for key,value in not_done_list.items()]
            list_dates=[datetime.strptime(date,'%Y-%m-%d') for date in list_string_dates]
            min_date=(min(list_dates))
            return {key:value for key,value in not_done_list.items() if db.date_to_status(value['date_to'])==min_date}
        else:
            return 'Type again',404

# to post a new task: requests.post('http:///127.0.0.1:5000/todo?ukol=ukolNr&body=body&date_to=YYYY-mm-dd')
@my_app.route('/todo/', methods=['POST'])
def todo():
    ukol= request.args.get('ukol')
    body=request.args.get('body')
    date_to=request.args.get('date_to')
    is_done='False'
    new_todos={
        ukol:{
        'body':body,
        'is_done':is_done,
        'date_to':date_to,
    }} 
    
    try:
        data=db.open_json()
    except FileNotFoundError:
        with open(db.DATA_FILE,"w", encoding='utf-8') as data_file:
            json.dump(new_todos,data_file,indent=4)
        return 'ok'
    else:
        data.update(new_todos)
        with open(db.DATA_FILE,"w", encoding='utf-8') as data_file:
            data=json.dump(data,data_file,indent=4)
        data=db.open_json()
        data=db.change_data(data)
        db.overwrite_json(data)
        print(data)
        return data

# delete a task: requests.delete('http:///127.0.0.1:5000/todo/ukolNr')
@my_app.route('/todo/<delete_ukol>', methods=['DELETE'])
def deleting(delete_ukol):
        
    try:
        data=db.open_json()
    except FileNotFoundError:
        return 'No file with items to delete',404
    else:
        try:
            del data[delete_ukol]
        except KeyError:
            return 'No data for %s ' % delete_ukol,400
        else:
            data=db.change_data(data)
            db.overwrite_json(data)
            print(data)
        return data

if __name__=='__main__':
    my_app.run(debug=True)