import models

from flask import Blueprint, request, jsonify 


from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict


goals = Blueprint('goals', 'goals')