"""
Документация модуля
"""

from flask import Flask
from flask_caching import Cache
from flask_restful import Api

from .config.config import FLASK_SECRET_KEY, inject_authorization, REDIS_URL

from .routes.api.answer import AnswersApi, AnswerApi
from .routes.api.database import TablesApi, TableApi
from .routes.api.question import QuestionsApi, QuestionApi

from .routes.web.main import main_bp
from .routes.web.login import login_bp
from .routes.web.logout import logout_bp
from .routes.web.question import question_bp
from .routes.web.register import register_bp
from .routes.web.statistic import statistic_bp
from .routes.web.question_update import question_update_bp
from .routes.web.answer_id import create_answer_id_bp
from .routes.web.question_id import create_question_id_bp
from .routes.web.question_all import create_question_all_bp


def create_app():
    """
    Документация функции
    """
    app = Flask(__name__)
    app.secret_key = FLASK_SECRET_KEY
    app.context_processor(inject_authorization)
    api = Api(app)

    cache = Cache(
        app,
        config={
            "CACHE_TYPE": "redis",
            "CACHE_REDIS_URL": f"{REDIS_URL}",
        },
    )

    api.add_resource(QuestionsApi, "/api/questions")
    api.add_resource(QuestionApi, "/api/questions/<int:id>")
    api.add_resource(AnswersApi, "/api/answers")
    api.add_resource(AnswerApi, "/api/answers/<int:id>")
    api.add_resource(TablesApi, "/api/tables")
    api.add_resource(TableApi, "/api/tables/<string:name>")

    app.register_blueprint(main_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(statistic_bp)
    app.register_blueprint(question_update_bp)
    app.register_blueprint(create_answer_id_bp(cache))
    app.register_blueprint(create_question_id_bp(cache))
    app.register_blueprint(create_question_all_bp(cache))

    return app
