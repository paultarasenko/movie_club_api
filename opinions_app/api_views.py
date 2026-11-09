from flask import jsonify, request

from . import app, db
from .models import Opinion
from .views import random_opinion

NOT_FOUND = {'error': 'Мнение не найдено'}


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    """Возвращает список мнений, можно фильтровать по title."""
    query = Opinion.query
    title = request.args.get('title')
    if title:
        query = query.filter(Opinion.title.ilike(f'%{title}%'))
    opinions = [opinion.to_dict() for opinion in query.all()]
    return jsonify({'opinions': opinions}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    """Создаёт новое мнение."""
    data = request.get_json(silent=True) or {}
    if 'title' not in data or 'text' not in data:
        return jsonify({'error': 'Поля title и text обязательны'}), 400
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201


@app.route('/api/opinions/random/', methods=['GET'])
def get_random_opinion():
    """Возвращает случайное мнение."""
    opinion = random_opinion()
    if opinion is None:
        return jsonify({'error': 'В базе нет мнений'}), 404
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    """Возвращает одно мнение по id."""
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify(NOT_FOUND), 404
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    """Обновляет переданные поля мнения."""
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify(NOT_FOUND), 404
    data = request.get_json(silent=True) or {}
    opinion.from_dict(data)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 200


@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    """Удаляет мнение."""
    opinion = db.session.get(Opinion, id)
    if opinion is None:
        return jsonify(NOT_FOUND), 404
    db.session.delete(opinion)
    db.session.commit()
    return '', 204
