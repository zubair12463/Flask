from flask import Flask, jsonify, request
import json
from pymongo import MongoClient
import json

# Add your MongoDB Details
MONGO_DB_URI = "mongodb+srv://zubairyt00:zubairyt00@cluster0.ikvfk8f.mongodb.net/"

MONGO_DB_NAME = 'ADVFN'
COLLECTION_NAME = 'insta1'

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]
collection = db[COLLECTION_NAME]

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        
        all_data = list(collection.find({}, {'_id': False}))

        per_page = 50
        link_filter = request.args.get('link')
        page = request.args.get('page', default=1, type=int)
        if link_filter:    
            filtered_data = [entry for entry in all_data if
                        (not link_filter or entry.get('instagram link') == link_filter)]

            for i in filtered_data:
                i.pop('id_', None)


            if not filtered_data:
                return jsonify({"message": "No matching data found."}), 404
            

            else:

                    total_pages = len(filtered_data) / per_page
                    if len(filtered_data) % per_page != 0:
                        total_pages += 1
                 
                    start_idx = (page - 1) * per_page
                    end_idx = start_idx + per_page
                    remaining_pages = total_pages - page
                    if len(filtered_data[start_idx:end_idx]) == 0:
                        return jsonify({"message": "No more data found."})
                    else:
                        return jsonify({
                            "data": filtered_data[start_idx:end_idx],
                            "remaining_pages": int(remaining_pages)
                        })
            

        else:
            total_pages = len(all_data) / per_page
            if len(all_data) % per_page != 0:
                total_pages += 1

            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            remaining_pages = total_pages - page
            if start_idx >= len(all_data):
                return jsonify({"message": "No more data found."})
            return jsonify({
                "data": all_data[start_idx:end_idx],
                "remaining_pages": int(remaining_pages)
            })
    

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
        