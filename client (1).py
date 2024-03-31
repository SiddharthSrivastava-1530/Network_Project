import pymongo

import speedtest
import asyncio




# db_link = "mongodb+srv://aayushnitinb:aayuanu2004@cluster0.enkpwvv.mongodb.net/speedTest?retryWrites=true&w=majority&appName=Cluster0"



client = pymongo.MongoClient("mongodb+srv://aayushnitinb:aayuanu2004@cluster0.enkpwvv.mongodb.net/speedTest?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database('speedTest')

collection = db['user_data']


async def measure_network():
    
    loop = asyncio.get_event_loop()
    st = speedtest.Speedtest()
    st.get_best_server()

    download_speed = await loop.run_in_executor(None, st.download)
    upload_speed = await loop.run_in_executor(None, st.upload)
    ping = st.results.ping
    ping_location = st.results.server['name'] if 'name' in st.results.server else "Unknown"

    return download_speed, upload_speed, ping, ping_location

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

    return dictionary

   
async def main():
    
    result = await get_network_status()
    collection.insert_one(result)
    
if __name__ == "__main__":
    asyncio.run(main())

    
