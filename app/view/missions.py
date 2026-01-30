from flask import jsonify, render_template, make_response
from flask_restful import Resource, reqparse
from app.models.missions import Missions

import datetime

# para adicionar
argumentos = reqparse.RequestParser()
argumentos.add_argument('name', type=str)
argumentos.add_argument('launch_date', type=str)
argumentos.add_argument('destination', type=str)
argumentos.add_argument('status', type=str)
argumentos.add_argument('tripulation', type=str)
argumentos.add_argument('util_charge', type=str)
argumentos.add_argument('duration', type=str)
argumentos.add_argument('cost', type=str)
argumentos.add_argument('status_descr', type=str)

# para visualizar por id
argumentos_view = reqparse.RequestParser()
argumentos_view.add_argument('id', type=str)

# para deletar
argumentos_delete = reqparse.RequestParser()
argumentos_delete.add_argument('id', type=str)

# para visualizar por data
argumentos_data = reqparse.RequestParser()
argumentos_data.add_argument('date_start', type=str)
argumentos_data.add_argument('date_end', type=str)

# para editar
argumentos_update = reqparse.RequestParser()
argumentos_update.add_argument('id', type=str)
argumentos_update.add_argument('name', type=str)
argumentos_update.add_argument('launch_date', type=str)
argumentos_update.add_argument('destination', type=str)
argumentos_update.add_argument('status', type=str)
argumentos_update.add_argument('tripulation', type=str)
argumentos_update.add_argument('util_charge', type=str)
argumentos_update.add_argument('duration', type=str)
argumentos_update.add_argument('cost', type=str)
argumentos_update.add_argument('status_descr', type=str)

class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)
        # return {'message': 'Hello World'}
    
class CreateMission(Resource):
    def post(self):
        dados = argumentos.parse_args()
        date_format = "%d/%m/%Y"
        launch_date = datetime.datetime.strptime(dados['launch_date'], date_format).date()
    
        Missions.save_mission(self, dados['name'], launch_date, 
                           dados['destination'], dados['status'],
                           dados['tripulation'], dados['util_charge'], 
                           dados['duration'], dados['cost'], dados['status_descr'])
        return "Missão cadastrada", 200
    
class ViewMissions(Resource):
    def get(self):
        return Missions.view_missions(self), 200
    
class ViewMission(Resource):
    def post(self):
        data = argumentos_view.parse_args()
        return Missions.view_mission(self, data['id'])

class DeleteMission(Resource):
    def delete(self):
        data = argumentos_delete.parse_args()
        return Missions.delete_mission(self, data['id'])
    
class ViewMissionPerDate(Resource):
    def post(self):
        data = argumentos_data.parse_args()
        date_format = "%d/%m/%Y"
        date_start = datetime.datetime.strptime(data['date_start'], date_format).date()
        date_end = datetime.datetime.strptime(data['date_end'], date_format).date()

        return Missions.view_mission_per_date(self, date_start, date_end)

class UpdateMission(Resource):
    def put(self):
        data = argumentos_update.parse_args()
        date_format = "%d/%m/%Y"
        launch_date = datetime.datetime.strptime(data['launch_date'], date_format).date()
    
        return Missions.update_mission(self, data['id'], data['name'], launch_date, 
                           data['destination'], data['status'],
                           data['tripulation'], data['util_charge'], 
                           data['duration'], data['cost'], data['status_descr'])