import pandas as pd
import numpy as np
import os
import re

from flask import Flask, request, jsonify, redirect, render_template, session
from flask_cors import CORS
from flask_session import Session


# Initialisation of a flask application
app = Flask(__name__)
config_settings = {
    'DEBUG': True,
    'SECRET_KEY': 'alkifwuhe589efwef6dfsdfegrwd5484fe69w',
    'SESSION_TYPE': 'filesystem',
    'SESSION_PERMANENT': False,
    'SESSION_COOKIE_SAMESITE': 'Lax',
    'SESSION_COOKIE_SECURE': False,
    'SESSION_COOKIE_HTTPONLY': False, #only here as I am using http for the testing
    } 
app.config.update(config_settings)
Session(app)
CORS(app, supports_credentials=True, origins=["http://localhost:5000", "http://127.0.0.1:5000"])

user_credentials = {'Alfred': 'test0', 'Farid': 'test1'}

log_pattern = re.compile(r'''^(?P<choice>.*?):\s
                             (?P<value>\d+)\s
                             euros\sadded\.\s
                             \((?P<date>\d{2}/\d{2}/\d{4}),
                             \s(?P<time>\d{2}:\d{2}:\d{2})\)\.''',re.VERBOSE)

@app.route('/')
def index():
    """
    Checking if the user has checked in before accessing the URL.
    """

    if 'username' in session:
        return redirect('/home')
    else:
        return render_template('login.html')
    
@app.route('/login', methods=['POST'])
def login():
    """
    To login.
    """

    data = request.json
    username = data.get('username').strip(" ")
    password = data.get('password')

    if username in user_credentials and user_credentials[username] == password:
        session['username'] = username

        print(f"logged in as: {session['username']}", flush=True)
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False})
    
@app.route('/logout', methods=['POST'])
def logout():
    """
    To be able to logout.
    """

    session.pop('username', None)
    return redirect('/')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('test_front_end.html')
    else:
        return redirect('/')
    
@app.route('/save-log', methods=['POST'])
def save_log():
    """
    To save the log from the front end for further analysis if needed.
    Also used as a data base.
    """
    log_pattern = re.compile(r'''^(?P<choice>.*?):\s
                             (?P<value>-?\d+)\s
                             euros\sadded\.\s
                             \((?P<day>\d{2})
                             /(?P<month>\d{2})
                             /(?P<year>\d{4}),
                             \s(?P<time>\d{2}:\d{2}:\d{2})\)\.''',re.VERBOSE)

    # # Saving data for log creation
    data = request.json
    newlog = data['logString']
    newcomment = 'none' if not data['logComment'] else data['logComment'] 
    raw_data = {
        'Username': session['username'],
        'Log': newlog,
        'Comment': newcomment,
        }
    raw_exists = os.path.exists('raw_data.csv')
    df_new = pd.DataFrame([raw_data])
    df_new.to_csv('raw_data.csv', mode='a', header=not raw_exists, index=False)

    # Saving data for statistics
    matching_pattern = log_pattern.match(newlog)
    if matching_pattern:
        new_values = {
            'Username': session['username'],
            'Choice': matching_pattern.group('choice'),
            'Value': matching_pattern.group('value'),
            'Year': matching_pattern.group('year'),
            'Month': matching_pattern.group('month'),
            'Day': matching_pattern.group('day'),
            'Time': matching_pattern.group('time'),
            'Comment': newcomment,
            }
        df_new_row = pd.DataFrame([new_values])

        file_exists = os.path.exists('ordered_data.csv')
        df_new_row.to_csv('ordered_data.csv', mode='a', header=not file_exists, index=False)
    else:
        raise ValueError("The log entries don't match with the back-end Python code.")
    return jsonify({'message': 'String saved successfully'}), 200

@app.route('/get-logs', methods=['GET'])
def get_logs():
    """
    To get the log values to display in the past transactions html box.
    """

    session_username = session.get('username')
    if os.path.exists('raw_data.csv'):
        df = pd.read_csv('raw_data.csv')

        usernames = df['Username'].tolist()
        logs = df['Log'].tolist()
        comments = df['Comment'].tolist()
    else:
        usernames = session_username
        logs = ['No transactions yet.']
        comments = ['No comments yet.']
    
    response_data = {
        'Session_username': session_username,
        'Usernames': usernames,
        'Logs': logs,
        'Comments': comments,
        }
    return jsonify(response_data)

@app.route('/get-comments', methods=['GET'])
def get_comments():
    """
    To only get the logs and comments for the logs that actually have a comment.
    """

    session_username = session.get('username')
    if os.path.exists('raw_data.csv'):
        df = pd.read_csv('raw_data.csv')
        filters = (df['Comment'] != 'none')
        usernames = df[filters]['Username'].tolist()
        logs = df[filters]['Log'].tolist()
        comments = df[filters]['Comment'].tolist()
    else:
        usernames = session_username
        logs = ['No transactions yet.']
        comments = ['No comments yet.']
    
    response_data = {
        'Session_username': session_username,
        'Usernames': usernames,
        'Logs': logs,
        'Comments': comments,
    }
    return jsonify(response_data)

@app.route('/get-summary', methods=['GET'])
def get_summary():
    """
    To get the summary of the transactions on the main page.
    """
    
    if os.path.exists('ordered_data.csv'):
        instance = Statistics(session.get('username'))
        data = instance.Data_giver_new()
    else:
        data = {
            'headerOrder': None,
            'data': None,
            }
    return jsonify(data)


class Statistics:
    """
    To set all the statistics done.
    """

    def __init__(self, username: str, stats: bool = False):
        self.data = pd.read_csv('ordered_data.csv')

        # Attributes
        self.Important_attributes(username)

        # Function choices

    def Important_attributes(self, username):
        """
        Function to store the important instance attributes.
        """
        
        self.usernames = ['Alfred', 'Farid']
        self.username = username
        for not_username in ['Alfred', 'Farid']:
            if self.username != not_username:
                self.not_username = not_username
                break


        self.month_name_list = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
            ]

    def Total_expenditures(self):
        """
        For the total money given and how much is needed.
        """

        other_username = [s for s in self.usernames if s!=self.username][0]

        username_euros = self.data[self.data['Username'] == self.username]['Value']
        other_username_euros = self.data[self.data['Username'] == other_username]['Value']

        if username_euros.any():
            total_given = username_euros.sum()
        else:
            total_given = 0
        if other_username_euros.any():
            total_taken = other_username_euros.sum()
        else:
            total_taken = 0
        return int(total_given), int(total_taken)
    
    def Total_choice_new(self):
        """
        To get the total sum of money given by both parties for a certain option.
        """

        user_choice_sum = self.data.groupby(['Username', 'Choice'])['Value'].sum().reset_index()
        choice_sum = self.data.groupby(['Choice'])['Value'].sum().reset_index()
        choice_sum['Username'] = 'Total'
        data_choice = pd.concat([user_choice_sum, choice_sum], ignore_index=True)
        total_sum = data_choice.groupby(['Username'])['Value'].sum().reset_index()
        total_sum['Choice'] = 'TOTAL'
        self.data_choice = pd.concat([data_choice, total_sum], ignore_index=True)
    
    def Total_choice(self, choice: str):
        """
        To get the total sum of money given by both parties for a certain option.
        """

        other_username = [s for s in self.usernames if s != self.username][0]
        username_choice = self.data[(self.data['Username'] == self.username) & (self.data['Choice'] == choice)]['Value']
        other_username_choice = self.data[(self.data['Username'] == other_username) & (self.data['Choice'] == choice)]['Value']
        if username_choice.any():
            username_given = username_choice.sum()
        else:
            username_given = 0
        if other_username_choice.any():
            other_username_given = other_username_choice.sum()
        else:
            other_username_given = 0
        return int(username_given), int(other_username_given)
    
    def Data_giver(self):
        """
        To get all the main values that will automatically be displayed on the /home page.
        """

        total_given, total_taken = self.Total_expenditures()
        rent_given, rent_taken = self.Total_choice('Rent')
        internet_given, internet_taken = self.Total_choice('Internet')
        electricity_given, electricity_taken = self.Total_choice('Electricity')
        gas_given, gas_taken = self.Total_choice('Gas')
        insurance_given, insurance_taken = self.Total_choice('Insurance')
        food_given, food_taken = self.Total_choice('Food')
        cat_given, cat_taken = self.Total_choice('Cat')
        utilities_given, utilities_taken = self.Total_choice('Utilities')
        other_given, other_taken = self.Total_choice('Other')
        
        values_dict = {
            'Rent': [rent_given, rent_taken, rent_given - rent_taken],
            'Internet': [internet_given, internet_taken, internet_given - internet_taken],
            'Electricity': [electricity_given, electricity_taken, electricity_given - electricity_taken],
            'Gas': [gas_given, gas_taken, gas_given - gas_taken],
            'Insurance': [insurance_given, insurance_taken, insurance_given - insurance_taken],
            'Food': [food_given, food_taken, food_given - food_taken],
            'Cat': [cat_given, cat_taken, cat_given - cat_taken],
            'Utilities': [utilities_given, utilities_taken, utilities_given - utilities_taken],
            'Other': [other_given, other_taken, other_given - other_taken],
            'TOTAL': [total_given, total_taken, total_given - total_taken],
            }
        
        header_order = list(values_dict.keys())
        return {'headerOrder': header_order, 'data': values_dict}
    
    def Data_giver_new(self):
        """
        To get all the main values that will automatically be displayed on the /home page.
        """
        self.Total_choice_new()

        username_order = [self.username, self.not_username, 'Total']
        pivot_df = self.data_choice.pivot(index='Choice', columns='Username', values='Value')
        pivot_df = pivot_df.reindex(columns=username_order)
        pivot_df.fillna(0, inplace=True) # swapping nans to zeros
        result_dict = pivot_df.apply(lambda row: row.tolist(), axis=1).to_dict()
        header_order = list(result_dict.keys())
        print(f"the header order is {header_order}")
        print(f"the values for the rent are {result_dict['Rent']}")
        return {'headerOrder': header_order, 'data': result_dict}
    
    def Monthly_integration(self):
        """
        To get the monthly total expenditure for a given choice.
        """

        monthly_sum = self.data.groupby(['Choice', 'Month'])['Value'].sum().reset_index()
        user_monthly_sum = self.data.groupby(['Choice', 'Month', 'Username'])['Value'].sum().reset_index()

        monthly_sum['Username'] = 'Total'
        return pd.concat([user_monthly_sum, monthly_sum], ignore_index=True)




if __name__ == '__main__':
    app.run(debug=True)