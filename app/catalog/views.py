from app import db
from app.catalog.models import Composer, Composition
from flask import Blueprint, render_template, redirect, request, url_for

bp = Blueprint("catalog", __name__)

@bp.route("/")
def index():
    # Get arguments from the query string
    opus_number = request.args.get("opus")
    movement_number = request.args.get("movement")
    title = request.args.get("title")
    key_signature = request.args.get("key")
    composer = request.args.get("composer")

    # Sort the compositions by composer, opus, and movement number
    select = db.select(Composition).order_by(
            Composition.composer_id,
            Composition.opus_number,
            Composition.movement_number)

    # Apply desired filters
    if opus_number:
        select = select.filter_by(opus_number=opus_number)
    if movement_number:
        select = select.filter_by(movement_number=movement_number)
    if title:
        select = select.filter(Composition.title.contains(title))
    if key_signature:
        select = select.filter_by(key_signature=key_signature)
    if composer:
        select = select.join(Composer, Composer.name.contains(composer))

    # Make the selection
    compositions = db.session.execute(select).scalars()

    # Render the index of compositions
    return render_template("catalog/index.html", compositions=compositions)

@bp.route("/add-composer", methods=["GET", "POST"])
def add_composer():
    # On POST requests, add a composer based on form data
    if request.method == "POST":
        name = request.form["name"]
        birthday = request.form["birthday"]
        db.session.add(Composer(name=name, birthday=birthday))
        db.session.commit()
        return redirect(url_for("catalog.index"))

    # On GET requests, just render the form
    return render_template("catalog/add-composer.html")

@bp.route("/add-composition", methods=["GET", "POST"])
def add_composition():
    # On POST requests, add a composition based on form data
    if request.method == "POST":
        opus_number = request.form["opus"]
        movement_number = request.form["movement"]
        title = request.form["title"]
        key_signature = request.form["key"]
        composer = Composer.query.get(request.form["composer"])
        url = request.form["url"]
        db.session.add(Composition(opus_number=opus_number, movement_number=movement_number, title=title, key_signature=key_signature, composer=composer, url=url))
        db.session.commit()
        return redirect(url_for("catalog.index"))

    # On GET requests, just render the form
    return render_template("catalog/add-composition.html")
