"""
Документация модуля
"""

import secrets

from flask import Flask
from flask_restful import Api

from routes.api.answer import AnswersApi, AnswerApi
from routes.api.question import QuestionsApi, QuestionApi

from routes.api.data_base import api_tables_bp, api_table_bp

from routes.web.main import main_bp
from routes.web.question import question_bp
from routes.web.question_update import question_update_bp
from routes.web.statistic import statistic_bp

app = Flask(__name__)
api = Api(app)
app.secret_key = secrets.token_hex(16)

api.add_resource(QuestionsApi, '/api/questions')
api.add_resource(QuestionApi, '/api/questions/<int:id>')
api.add_resource(AnswersApi, '/api/answers')
api.add_resource(AnswerApi, '/api/answers/<int:id>')

app.register_blueprint(api_tables_bp)
app.register_blueprint(api_table_bp)

app.register_blueprint(main_bp)
app.register_blueprint(question_bp)
app.register_blueprint(question_update_bp)
app.register_blueprint(statistic_bp)

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
