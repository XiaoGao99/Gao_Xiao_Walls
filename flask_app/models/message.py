from flask_app.config.mysqlconnection import connectToMySQL
class Message:
    def __init__(self, data):
        self.id = data['id']
        self.descrip = data['descrip']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.time = ""
    
    @classmethod
    def save(cls, data):
        query = "insert into messages(descrip, name, user_id) values(%(descrip)s, %(name)s, %(receiver_id)s);"
        return connectToMySQL("wall").query_db(query,data)
    
    @classmethod
    def delete(cls, data):
        query = "delete from messages where id = %(id)s"
        return connectToMySQL("wall").query_db(query, data)


    

        