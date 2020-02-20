import models

from flask import Blueprint, request, jsonify 


from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict


goals = Blueprint('goals', 'goals')


#create goals route
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


#view all goals route
@goals.route('/', methods=['GET'])
@login_required
def current_user_goals():
	current_user_goals_dicts = [model_to_dict(goal) for goal in current_user.goals]
	
	return jsonify(
		data=current_user_goals_dicts,
		message=f'Got current user goals {len(current_user_goals_dicts)}',
		status=200),200


#delete goals route
@goals.route('/<id>', methods=['Delete'])
@login_required
def delete_goal(id):
	goal_to_delete = models.Goal.get_by_id(id)
	if current_user.id == goal_to_delete.owner.id:
		goal_to_delete.delete_instance()
		

		return jsonify(
			data={},
			message="Deleted Your goal",
			status=200),200
	else:
		return jsonify(
			data={
				'error' : 'Forbidden'
			},
			message="You cant delete this goal",
			status=403), 403



@goals.route('/<id>', methods=['PUT'])
@login_required
def update_goal(id):
	payload = request.get_json()

	goal = models.Goal.get_by_id(id)

	if goal.owner.id == current_user.id:
		if 'title' in payload:
			goal.title=payload['title']
		if 'deadline' in payload:
			goal.deadline = payload['deadline']
		if 'description' in payload:
			goal.description = payload['description']
		if 'before_deadline' in payload:
			goal.before_deadline = payload['before_deadline']
		goal.save()

		goal_dict= model_to_dict(goal)

		return jsonify(data=goal_dict,
			message='Your update was successfull',
			status=200),200
	else:
		return jsonify(
			data={
				'error': 'Forbidden'
			},message='Cant update this goal', status=403),403













