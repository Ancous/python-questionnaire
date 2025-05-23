"""
Документация модуля
"""

import secrets

from flask import Flask

from routes.api.question import api_questions_bp
from routes.api.table import api_tables_bp
from routes.web.answer import answer_bp
from routes.web.main import main_bp
from routes.web.question import question_bp
from routes.web.question_update import question_update_bp
from routes.web.statistic import statistic_bp

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.register_blueprint(api_questions_bp)
app.register_blueprint(api_tables_bp)
app.register_blueprint(answer_bp)
app.register_blueprint(main_bp)
app.register_blueprint(question_bp)
app.register_blueprint(question_update_bp)
app.register_blueprint(statistic_bp)

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
