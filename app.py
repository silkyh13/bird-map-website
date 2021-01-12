"""
A sample Hello World server.
"""
import os
import requests

from flask import Flask, render_template, json, jsonify,request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# pylint: disable=C0103
app = Flask(__name__)
CORS(app)
from bird import Bird
from reset_data import ResetData
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:5Eespgmbtct40iOJ@34.69.244.156/bird_database_test'
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:5Eespgmbtct40iOJ@34.69.244.156/bird_database_test'


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True, pool_pre_ping=True)
 
Session = sessionmaker()
Session.configure(bind=engine)
# session = Session()

def get_metadata(item_name):
    metadata_url = 'http://metadata.google.internal/computeMetadata/v1/'
    headers = {'Metadata-Flavor': 'Google'}

    try:
        r = requests.get(metadata_url + item_name, headers=headers)
        return r.text
    except:
        return 'Unavailable'


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's redeployed!"

    project = get_metadata('project/project-id')
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Project=project,
        Service=service,
        Revision=revision)

@app.route('/test', methods=['GET', 'POST'])
def bird_data():
    # bird_data_path = os.path.join(app.root_path, "data", "bird_data.json")
    # loader = json.load(open(bird_data_path))
    if request.method == 'GET':
        bird_data_path = os.path.join(app.root_path, "data", "unified_bird_data.json")
        loader = json.load(open(bird_data_path))
        return jsonify(loader)
        



@app.route('/bird/<endpoint>', methods=["GET", "PUT"])
def get_bird(endpoint):
    #query for specific bird  
    session = Session()
    if request.method == "GET":
        bird_object = session.query(Bird).filter(Bird.id == endpoint).first()
        parsed_bird_data = return_stringify_bird(bird_object)
        return jsonify(parsed_bird_data)
    elif request.method == "PUT":
        return handle_update_bird(endpoint, request)


@app.route("/bird", methods=["GET", "POST"])
def bird():
   if request.method == "GET":
       return handle_get_bird(request)
   elif request.method == "POST":
       return handle_create_bird(request)
   else:
       return "how did you get here?"

def handle_update_bird(endpoint, request):
    #copy of the origina bird data
    print('what info was being passed',endpoint, request.json["name"])
    session = Session()
    (session.query(Bird)
            .filter(Bird.id == endpoint.encode("utf-8", errors="ignore"))
            .update({
                Bird.name:request.json["name"].encode("utf-8", errors="ignore"),
                Bird.image:request.json["image"].encode("utf-8", errors="ignore"),
                Bird.description:request.json["description"].encode("utf-8", errors="ignore"),
                Bird.life_history:request.json["life_history"].encode("utf-8", errors="ignore"),
                Bird.distribution_and_habitat:request.json["distribution_and_habitat"].encode("utf-8", errors="ignore"),
                Bird.management_and_research_needs:request.json["management_and_research_needs"].encode("utf-8", errors="ignore"),
                Bird.locations:stringify_list(request.json["locations"])
            }, synchronize_session = False)
    )
    session.commit()
   
    bird_object = session.query(Bird).filter(Bird.id == endpoint).first()
    parsed_bird_data = return_stringify_bird(bird_object)
    return jsonify(parsed_bird_data)
            
def handle_get_bird(request):
    session = Session()
    birds = session.query(Bird).all()
    return jsonify(render_bird_json(birds))

def return_stringify_bird(bird): 
    return {
            'id': bird.id,
            'name': bird.name,
            'image': bird.image,
            'description': bird.description,
            'life_history': bird.life_history,
            'distribution_and_habitat': bird.distribution_and_habitat,
            'status': bird.status,
            'management_and_research_needs': bird.management_and_research_needs,
            'locations': bird.locations.split(";") 
    }

def render_bird_json(birds):
   return {
       'data': [{
           'id': bird.id,
           'name': bird.name,
           'image': bird.image,
           'description': bird.description,
           'life_history': bird.life_history,
           'distribution_and_habitat': bird.distribution_and_habitat,
           'status': bird.status,
           'management_and_research_needs': bird.management_and_research_needs,
           'locations': bird.locations.split(";")
       } for bird in birds]
   }
   
def stringify_list(location_array): 
    stringed_list = ""
    for i, location in enumerate(location_array):
        if (i < len(location_array)-1):
            stringed_list = stringed_list + location + ';'
        else:
            stringed_list = stringed_list + location 
    return stringed_list

def handle_create_bird(request):
    session = Session()
    imageUrl = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimg.buzzfeed.com%2Fbuzzfeed-static%2Fstatic%2F2017-08%2F1%2F11%2Fasset%2Fbuzzfeed-prod-fastlane-01%2Fsub-buzz-3083-1501601080-1.jpg&f=1&nofb=1"
    
    if request.json["image"]:
        imageUrl = request.json["image"]
    data = Bird(
            id=request.json["id"].encode("utf-8", errors="ignore"), 
            name=request.json["name"].encode("utf-8", errors="ignore"), 
            image=imageUrl.encode("utf-8", errors="ignore"),  
            description=request.json["description"].encode("utf-8", errors="ignore"),  
            life_history=request.json["life_history"].encode("utf-8", errors="ignore"), 
            distribution_and_habitat=request.json["distribution_and_habitat"].encode("utf-8", errors="ignore"), 
            status=request.json["status"].encode("utf-8", errors="ignore"), 
            management_and_research_needs=request.json["management_and_research_needs"].encode("utf-8", errors="ignore"), 
            locations=stringify_list(request.json["locations"]),
    )
    session.add(data)
    session.commit()
    return {"success":True, "id": request.json["id"]}

@app.route("/reset-data", methods=["POST"])
def resetData():
    session = Session()
    obj = ResetData(app, session)
    obj.reset_data()
    return jsonify({"success":True })

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')

