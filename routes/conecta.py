from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.utils import secure_filename

import os
import uuid

from models.conecta import (
    listar_posts,
    salvar_post
)

conecta_bp = Blueprint("conecta", __name__)


@conecta_bp.route("/conecta")
def conecta():

    posts = listar_posts()

    return render_template(
        "conecta.html",
        posts=posts
    )