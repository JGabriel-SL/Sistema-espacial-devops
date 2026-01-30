from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_restful import Api 
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

from app.view.missions import Index, CreateMission, ViewMissions, ViewMission, DeleteMission, ViewMissionPerDate, UpdateMission
api.add_resource(Index, '/') 
api.add_resource(CreateMission, '/create_mission')
api.add_resource(ViewMissions, '/view_missions')
api.add_resource(ViewMission, '/view_mission')
api.add_resource(DeleteMission, '/delete_mission')
api.add_resource(ViewMissionPerDate, '/view_missions_per_date')
api.add_resource(UpdateMission, '/update_mission')