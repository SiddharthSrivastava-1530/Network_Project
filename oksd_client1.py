from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import pymongo

import speedtest
import asyncio


app = Flask(__name__)
CORS(app)

# db_link = "mongodb+srv://aayushnitinb:aayuanu2004@cluster0.enkpwvv.mongodb.net/speedTest?retryWrites=true&w=majority&appName=Cluster0"


client = pymongo.MongoClient(
    "mongodb+srv://aayushnitinb:aayuanu2004@cluster0.enkpwvv.mongodb.net/speedTest?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database('speedTest')

collection = db['speedData']
user_data = db['user_data']


async def measure_network():
    loop = asyncio.get_event_loop()
    st = speedtest.Speedtest()
    st.get_best_server()

    download_speed = await loop.run_in_executor(None, st.download)
    upload_speed = await loop.run_in_executor(None, st.upload)
    ping = st.results.ping
    ping_location = st.results.server['name'] if 'name' in st.results.server else "Unknown"

    return download_speed, upload_speed, ping, ping_location



@app.route('/', methods=['GET'])
async def get_network_status():
    download_speed, upload_speed, ping, ping_location = await measure_network()

    # Calculate bandwidth in Mbps
    bandwidth = download_speed + upload_speed

    dictionary = {
                'user':'user1',
                'download_speed': download_speed / 1024 / 1024,
                'upload_speed': upload_speed / 1024 / 1024,
                'ping': ping,
                'ping_location': ping_location,
                'bandwidth': bandwidth / 1024 / 1024
                }

    user_data.insert_one(dictionary)

    first_five_elements = collection.find().limit(5)

    return jsonify({
        'user':'user1',
        'download_speed': download_speed / 1024 / 1024,  # Convert to Mbps
        'upload_speed': upload_speed / 1024 / 1024,  # Convert to Mbps
        'ping': ping,
        'ping_location': ping_location,
        'bandwidth': bandwidth / 1024 / 1024  # Convert to Mbps
    })


# @app.route('/network/status/user', methods=['GET'])
# async def user():
#     random_documents = collection.aggregate([{"$sample": {"size": 5}}])
#     random_documents_list = list(random_documents)
#     # Convert ObjectId to string representation
#     for doc in random_documents_list:
#         doc['_id'] = str(doc['_id'])
#     print(random_documents_list[2])
#     return jsonify(random_documents_list)


# @app.route('/network/status/user1', methods=['GET'])
# async def user1():

#     user_one = user_data.find_one({'user':'user1'},sort=[("_id", pymongo.DESCENDING)])

#     dictionary = {}


#     dictionary = {
#             'download_speed': user_one['download_speed'],
#             'upload_speed': user_one['upload_speed'],
#             'ping': user_one['ping'],
#             'ping_location': "MyServer",
#             'bandwidth': user_one['bandwidth']
#         }


#     return jsonify(dictionary)




# @app.route('/network/status/user2', methods=['GET'])
# async def user2():

#     user_one = user_data.find_one({'user':'user2'},sort=[("_id", pymongo.DESCENDING)])

#     dictionary = {}


#     dictionary = {
#             'download_speed': user_one['download_speed'],
#             'upload_speed': user_one['upload_speed'],
#             'ping': user_one['ping'],
#             'ping_location': "MyServer",
#             'bandwidth': user_one['bandwidth']
#         }


#     return jsonify(dictionary)



# @app.route('/network/status/user3', methods=['GET'])
# async def user3():

#     user_one = user_data.find_one({'user':'user3'},sort=[("_id", pymongo.DESCENDING)])

#     dictionary = {}


#     dictionary = {
#             'download_speed': user_one['download_speed'],
#             'upload_speed': user_one['upload_speed'],
#             'ping': user_one['ping'],
#             'ping_location': "MyServer",
#             'bandwidth': user_one['bandwidth']
#         }


#     return jsonify(dictionary)




# @app.route('/network/status/client_info', methods=['GET'])
# async def client_data():
#     distinct_users = user_data.distinct("user")

#     download_speed = 0
#     upload_speed = 0
#     ping = 0
#     ping_location = None
#     bandwidth = 0

#     st = speedtest.Speedtest()
#     st.get_best_server()
#     ping_location = st.results.server['name'] if 'name' in st.results.server else "Unknown"


#     for user in distinct_users:
#         user_cursor = user_data.find({'user':user})
#         for document in user_cursor:
#             print(document)
#             download_speed +=document['download_speed']
#             upload_speed += document['upload_speed']
#             ping += document['ping']/len(distinct_users)
#             bandwidth += document['download_speed'] + document['upload_speed']
#             print(download_speed)


#     dict = {
#         'download_speed': download_speed,
#         'upload_speed': upload_speed,
#         'ping': ping,
#         'ping_location': ping_location,
#         'bandwidth': bandwidth
#     }
    
#     return jsonify(dict)




if __name__ == '__main__':
    app.run(debug=True)
