"""
Документация модуля
"""

from flask import session, Blueprint, redirect, url_for

logout_bp = Blueprint(
    "logout",
    __name__,
    url_prefix="/logout"
)


@logout_bp.route('/', methods=['GET'])
def logout():
    """
    Документация функции
    """
    session.clear()
    return redirect(url_for('main.main'))
