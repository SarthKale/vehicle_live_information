from flask import Flask, request
import pymongo
import datetime


app = Flask(__name__)


def db_connection(collection_name):
    connection = pymongo.MongoClient("mongodb://db:27017") # MongoDB Connection
    db = connection['vehicle_info'] # Database access variable
    collection = db[collection_name] # Collection (table) access variable
    return collection

@app.route('/admin/add', methods=['POST'])
def add_admin():
    if request.method == 'POST':
        posted_data = request.get_json()
        admin_username = posted_data['admin_username']
        admin_password = posted_data['admin_password']
        admin_name = posted_data['admin_name']
        if not isinstance(admin_username, str):
            return {"status": "303", "message": "Invalid Input : {} for admin_username, ideal_type : <class 'str'>, actual_type : {}".format(admin_username,  type(admin_username))}
        if not isinstance(admin_password, str):
            return {"status": "303", "message": "Invalid Input : {} for admin_password, ideal_type : <class 'str'>, actual_type : {}".format(admin_password,  type(admin_password))}
        if not isinstance(admin_name, str):
            return {"status": "303", "message": "Invalid Input : {} for admin_name, ideal_type : <class 'str'>, actual_type : {}".format(admin_name,  type(admin_name))}
        admin_docs = db_connection('admin_docs')
        if admin_docs.count_documents({'username': admin_username}) > 0:
            return {"status": "306", "message": "Admin user already exists"}
        else:
            admin_docs.insert_one({
                'username': admin_username, 'password': admin_password, 'name': admin_name
            })
            return {"status": "200", "message": "OK"}


@app.route('/register', methods=["POST"])
def registration():
    if request.method == 'POST':
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        name = posted_data['name']
        mobile_number = posted_data['mobile_number']
        if not isinstance(username, str):
            return {"status": "303", "message": "Invalid Input : {} for username, ideal_type : <class 'str'>, actual_type : {}".format(username,  type(username))}
        if not isinstance(password, str):
            return {"status": "303", "message": "Invalid Input : {} for password, ideal_type : <class 'str'>, actual_type : {}".format(password,  type(password))}
        if not isinstance(name, str):
            return {"status": "303", "message": "Invalid Input : {} for name, ideal_type : <class 'str'>, actual_type : {}".format(name,  type(name))}
        if not isinstance(mobile_number, int):
            return {"status": "303", "message": "Invalid Input : {} for mobile_number, ideal_type : <class 'int'>, actual_type : {}".format(mobile_number,  type(mobile_number))}
        user_docs = db_connection('user_docs')
        if user_docs.count_documents({'username': username}) > 0:
            return {"status": "300", "message": "User already exists!"}
        else:
            user_docs.insert_one({
                'username': username, 'password': password, 'name': name, 'mobile_number': mobile_number
            })
            return {"status": "200", "message": "OK"}


@app.route('/vehicle/add', methods=["POST"])
def add_vehicle():
    if request.method == "POST":
        posted_data = request.get_json()
        chessis_number = posted_data['chessis_number']
        registration_number = posted_data['registration_number']
        make = posted_data['make']
        model = posted_data['model']
        username = posted_data['username']
        admin_password = posted_data['admin_password']
        if not isinstance(chessis_number, str):
            return {"status": "303", "message": "Invalid Input : {} for chessis_number, ideal_type : <class 'str'>, actual_type : {}".format(chessis_number,  type(chessis_number))}
        if not isinstance(registration_number, str):
            return {"status": "303", "message": "Invalid Input : {} for registration_number, ideal_type : <class 'str'>, actual_type : {}".format(registration_number,  type(registration_number))}
        if not isinstance(make, str):
            return {"status": "303", "message": "Invalid Input : {} for make, ideal_type : <class 'str'>, actual_type : {}".format(make,  type(make))}
        if not isinstance(model, str):
            return {"status": "303", "message": "Invalid Input : {} for model, ideal_type : <class 'str'>, actual_type : {}".format(model,  type(model))}
        if not isinstance(username, str):
            return {"status": "303", "message": "Invalid Input : {} for username, ideal_type : <class 'str'>, actual_type : {}".format(username,  type(username))}
        if not isinstance(admin_password, str):
            return {"status": "303", "message": "Invalid Input : {} for admin_password, ideal_type : <class 'str'>, actual_type : {}".format(admin_password,  type(admin_password))}
        admin_docs = db_connection('admin_docs')
        if admin_docs.count_documents({'password': admin_password}) == 0:
            return {"status": "302", "message": "Invalid Admin Password"}
        user_docs = db_connection('user_docs')
        if user_docs.count_documents({'username': username}) == 0:
            return {"status": "301", "message": "User not found: {}".format(username)}
        vehicle_docs = db_connection('vehicle_docs')
        if vehicle_docs.count_documents({'chessis_number': chessis_number}) > 0:
            return {"status": "300", "message": "Vehicle with chessis number : {}, already exists".format(chessis_number)}
        else:
            vehicle_docs.insert_one({
                'chessis_number': chessis_number, 'registration_number': registration_number, 'make': make, 'model': model,
                'date_of_purchase': str(datetime.datetime.now().date()), 'service_history': [], 'sensors': {}
            })
            return {"status": "200", "message": "OK"}


@app.route('/vehicle/service', methods=["POST"])
def add_vehicle_service_data():
    if request.method == "POST":
        posted_data = request.get_json()
        username = posted_data['username']
        admin_password = posted_data['admin_password']
        chessis_number = posted_data['chessis_number']
        service_type = posted_data['service_type']
        if 'description' in list(dict(posted_data).keys()):
            description = posted_data['description']
        else:
            description = ""
        if not isinstance(username, str):
            return {"status": "303", "message": "Invalid Input : {} for username, ideal_type : <class 'str'>, actual_type : {}".format(username,  type(username))}
        if not isinstance(admin_password, str):
            return {"status": "303", "message": "Invalid Input : {} for admin_password, ideal_type : <class 'str'>, actual_type : {}".format(admin_password,  type(admin_password))}
        if not isinstance(chessis_number, str):
            return {"status": "303", "message": "Invalid Input : {} for chessis_number, ideal_type : <class 'str'>, actual_type : {}".format(chessis_number,  type(chessis_number))}
        if not isinstance(service_type, str):
            return {"status": "303", "message": "Invalid Input : {} for service_type, ideal_type : <class 'str'>, actual_type : {}".format(service_type,  type(service_type))}
        if not isinstance(description, str):
            return {"status": "303", "message": "Invalid Input : {} for description, ideal_type : <class 'str'>, actual_type : {}".format(description,  type(description))}
        admin_docs = db_connection('admin_docs')
        if admin_docs.count_documents({'password': admin_password}) == 0:
            return {"status": "302", "message": "Invalid Admin Password"}
        user_docs = db_connection('user_docs')
        if user_docs.count_documents({'username': username}) == 0:
            return {"status": "301", "message": "User not found: {}".format(username)}
        vehicle_docs = db_connection('vehicle_docs')
        if vehicle_docs.count_documents({'chessis_number': chessis_number}) == 0:
            return {"status": "304", "message": "Vehicle with chessis number: {}, does not exists".format(chessis_number)}
        elif vehicle_docs.count_documents({'chessis_number': chessis_number, 'username': username}) == 0:
            return {"status": "307", "message": "Vehicle with chessis_number {} does not belong to the user {}".format(chessis_number, username), "data": dict(vehicle_docs.find({'chessis_number': chessis_number}))}
        else:
            vehicle_info = dict(vehicle_docs.find({'chessis_number': chessis_number, 'username': username})[0])
            service_count = len(vehicle_info['service_history']) + 1
            service_data = vehicle_info['service_history']
            # date_of_service, service_count, service_type, description
            service_data.append({
                'date_of_service': str(datetime.datetime.now().date()), 'service_count': service_count, 'service_type': service_type, 'description': description
            })
            vehicle_docs.update_one(filter={'chessis_number': chessis_number, 'username': username}, update={'$set': {
                'service_history': service_data
            }})
            return {"status": "200", "message": "OK"}


@app.route('/sensor/update', methods=["PUT"])
def update_sensor_data():
    if request.method == "PUT":
        posted_data = request.get_json()
        chessis_number = posted_data['chessis_number']
        sensor_name = posted_data['name']
        sensor_value = posted_data['value']
        if not isinstance(chessis_number, str):
            return {"status": "303", "message": "Invalid Input : {} for chessis_number, ideal_type : <class 'str'>, actual_type : {}".format(chessis_number,  type(chessis_number))}
        vehicle_docs = db_connection('vehicle_docs')
        if vehicle_docs.count_documents({'chessis_number': chessis_number}) == 0:
            return {"status": "304", "message": "Vehicle with chessis number: {}, does not exists".format(chessis_number)}
        vehicle_docs.update_one({'chessis_number': chessis_number}, {'$set': {
            'sensors.{}'.format(sensor_name): sensor_value
        }})
        return {"status": "200", "message": "OK"}


@app.route('/vehicle/details', methods=["GET"])
def get_vehicle_details():
    if request.method == "GET":
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        chessis_number = posted_data['chessis_number']
        if not isinstance(username, str):
            return {"status": "303", "message": "Invalid Input : {} for username, ideal_type : <class 'str'>, actual_type : {}".format(username,  type(username))}
        if not isinstance(password, str):
            return {"status": "303", "message": "Invalid Input : {} for password, ideal_type : <class 'str'>, actual_type : {}".format(password,  type(password))}
        if not isinstance(chessis_number, str):
            return {"status": "303", "message": "Invalid Input : {} for chessis_number, ideal_type : <class 'str'>, actual_type : {}".format(chessis_number,  type(chessis_number))}
        user_docs = db_connection('user_docs')
        if user_docs.count_documents({'username': username}) == 0:
            return {"status": "301", "message": "User not found: {}".format(username)}
        if user_docs.count_documents({'password': password}) == 0:
            return {"status": "305", "message": "Invalid password entered for username : {}".format(username)}
        vehicle_docs = db_connection('vehicle_docs')
        if vehicle_docs.count_documents({'chessis_number': chessis_number}) == 0:
            return {"status": "304", "message": "Vehicle with chessis number: {}, does not exists".format(chessis_number)}
        vehicle_data = vehicle_docs.find_one({'chessis_number': chessis_number})
        return {"status": "200", "message": "OK"}


@app.route('/')
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

