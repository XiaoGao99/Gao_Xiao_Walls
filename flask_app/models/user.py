
from flask_app.models.message import Message
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.message = []
        self.count = 0

    @classmethod
    def get_all(cls):
        query = "select * from users order by first_name asc;"
        results = connectToMySQL('wall').query_db(query)
        users = []
        for user in results:
            users.append(user)
        return users
    
    @classmethod
    def get_one(cls, data):
        query = "select * from users where email = %(email)s;"
        results = connectToMySQL('wall').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "select * from users where id = %(id)s;"
        results = connectToMySQL('wall').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = "insert into users(first_name, last_name, email, password) \
            values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('wall').query_db(query,data)
    
    @classmethod
    def get_message(cls,data):
        query = "select * from users left join messages on users.id = messages.user_id\
            where users.id = %(id)s order by messages.created_at asc"
        results = connectToMySQL('wall').query_db(query,data)
        user = cls(results[0])
        for row in results:  
            if row['name'] != None:
                user.count += 1        
            message_data = {
                'id' : row['messages.id'],
                'name' : row['name'],
                'descrip' : row['descrip'],              
                'created_at' : row['messages.created_at'],
                'updated_at' : row['messages.updated_at'],
            }
            user.message.append(Message(message_data))
        return user

    @staticmethod
    def validate(user):
        valid = True 
        query = "select * from users where email = %(email)s;" 
        result = connectToMySQL("wall").query_db(query,user)
        if len(result) > 0:
            flash("Account already exist!","reg")
            valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters!", "reg")
            valid = False       
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters!", "reg")
            valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!", "reg")
            valid = False
        if len(user['email']) < 1:
            flash("Email must be provided!", "reg")
            valid = False
        if user['password'] != user['confirm'] :
            flash("Password does not match!", "reg")
            valid = False
        return valid
        

    



