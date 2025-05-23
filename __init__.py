"""
Документация модуля
"""

import secrets

from flask import Flask

from route.api.route_table_question_update import api_tables_questions_bp
from route.api.route_tables_all_remove import api_tables_bp
from route.web.route_answer import answer_bp
from route.web.route_main import main_bp
from route.web.route_questions import questions_bp
from route.web.route_questions_update import questions_update_bp
from route.web.route_statistics import statistics_bp

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.register_blueprint(api_tables_questions_bp)
app.register_blueprint(api_tables_bp)
app.register_blueprint(answer_bp)
app.register_blueprint(main_bp)
app.register_blueprint(questions_bp)
app.register_blueprint(questions_update_bp)
app.register_blueprint(statistics_bp)
