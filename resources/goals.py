import models

from flask import Blueprint, request, jsonify 


from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict


goals = Blueprint('goals', 'goals')

@goals.route('/', methods=['POST'])
@login_required
def create_goal():
	payload = request.get_json()
	goal = models.Goal.create(
		title=payload['title'],
		owner=current_user.id,
		description= payload['description'],
		deadline=payload['deadline'],
		before_deadline=payload['before_deadline']
		)
	goal_dict = model_to_dict(goal)

	return jsonify(
		data=goal_dict,
		message='You made a goal',
		status=201),201