from flask import Blueprint, render_template, request

from src.models import Post

main = Blueprint("main", __name__)


@main.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("index.html", posts=post)


# @main.route("/about/")
# def about():
#     return render_template("index.html")
