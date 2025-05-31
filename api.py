# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)
# api = Api(app)


# class UserModel(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(80), unique = True, nullable = False)
#     email = db.Column(db.String(80), unique = True, nullable = False)

#     def __repr__(self):
#         return f"User(name = {self.name}, email = {self.email} )"

# user_args = reqparse.RequestParser()
# user_args.add_argument('name', type = str, required = True , help = " Name cannot be empty")
# user_args.add_argument('email', type = str, required = True , help = " Email cannot be empty")

# class Users(Resource):
#     def get(self):
#         users = UserModel.query.all()
#         return users
    
# api.add_resource(Users, '/api/users/')

# @app.route('/')
# def home():
#     return '<h1>Hello</h1>'

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class ContactsModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    address = db.Column(db.String(300), nullable = True)
    phone = db.Column(db.String(10), nullable = False)

    def __rept__(self):
        return f"name : {self.name}, phone : {self.phone}, addresss : {self.address}"


# contacts = {
#     1 : {"name" : "Swastik", 
#        "phone" : "9339999339", 
#        "address" : "168/5 rifle club"},

#     2 : {"name" : "Dilip", 
#        "phone" : "9339988839", 
#        "address" : "1/5 ranna club"}
#         }

resource_fields = {
    "id" : fields.Integer,
    "name" : fields.String,
    "phone" : fields.String,
    "address" : fields.String
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("name", type = str, help = "name must not be empty", required = True)
task_post_args.add_argument("phone", type = str, help = "Phone must not be empty", required = True)
task_post_args.add_argument("address", type = str)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("name", type = str)
task_put_args.add_argument("phone", type = str)
task_put_args.add_argument("address", type = str)


class ContactManagementAll(Resource):
    #@marshal_with(resource_fields) not needed
    def get(self):
        contacts = ContactsModel.query.all()
        con = {}
        for contact in contacts:
            con[contact.id] = {
            "name" : contact.name,
            "phone" : contact.phone,
            "address" : contact.address
}
        return con
    
class ContactManagement(Resource):
    @marshal_with(resource_fields)
    def get(self, con_id):
        con = ContactsModel.query.filter_by(id = con_id).first()
        return con
    
    @marshal_with(resource_fields)
    def post(self, con_id):
        args = task_post_args.parse_args()   #this receives and checks the json post resource/data
        contact = ContactsModel.query.filter_by(id = con_id).first()
        if contact:
            abort(409, message = "contact id is taken ... ")
        con = ContactsModel(id = con_id, name = args["name"], phone = args["phone"], address = args["address"])
        db.session.add(con)
        db.session.commit()
        return con, 201
    
    @marshal_with(resource_fields)
    def delete(self, con_id):
        contact = ContactsModel.query.filter_by(id = con_id).first()
        db.session.delete(contact)
        db.session.commit()
        return 'Contact deleted', 204
    
    #@marshal_with(resource_fields)
    def put(self, con_id):
        args = task_put_args.parse_args()
        contact = ContactsModel.query.filter_by(id = con_id).first()
        if not contact:
            abort(404, message = "id not found")

        if args["name"]:
            contact.name = args["name"]
        if args["phone"]:
            contact.phone = args["phone"]
        if args["address"]:
            contact.address = args["address"]
        db.session.commit()
        return contact #this will be returned in the j son format due to marshalling
    

api.add_resource(ContactManagement, '/contacts/<int:con_id>')
api.add_resource(ContactManagementAll, '/contacts')




if __name__ == '__main__':
    app.run(debug=True)