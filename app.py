import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # store users name and role and course
                session["user"] = existing_user["username"]
                session["role"] = existing_user["role"]
                session["course"] = existing_user["assigned_course"]
                username = session["user"]
                flash("Welcome, {}".format(username))
                course = session.get("course")
                return render_template(
                    "profile.html", username=username, course=course)

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/get_lessons")
def get_lessons():
    lessons = list(mongo.db.lessons.find())
    return render_template("lessons.html", lessons=lessons)


@app.route("/users")
def get_users():
    users = list(mongo.db.users.find())
    if session.get("role") == "admin":
        return render_template("users.html", users=users)

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    course = session.get("course")

    if session["user"]:
        return render_template(
            "profile.html", username=username, course=course)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove session cookies
    flash("You have been logged out")
    session.pop("user")
    session.pop("role")
    session.pop("course")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # is Email already taken?
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Email already in use")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "role": request.form.get("role"),
            "status": "pending",
            "assigned_course": "pending",
            "enrollment_day": "pending"
        }
        mongo.db.users.insert_one(register)

        # Store user in session cookies
        session["user"] = request.form.get("username").lower()
        session["role"] = request.form.get("role")
        session["course"] = "pending"
        flash("Registration Successful!")
        return redirect(url_for(
            "profile", username=session["user"], course=session["course"]))

    return render_template("register.html")


@app.route("/add_lesson", methods=["GET", "POST"])
def add_lesson():
    if request.method == "POST":
        is_mandatory = "on" if request.form.get("is_mandatory") else "off"
        has_audio = "on" if request.form.get("has_audio") else "off"
        has_video = "on" if request.form.get("has_video") else "off"
        has_submission = "on" if request.form.get("has_submission") else "off"
        text_answer = "on" if request.form.get("text_answer") else "off"
        file_answer = "on" if request.form.get("file_answer") else "off"
        lesson_video = request.form.get("lesson_video").replace(
            "https://www.youtube.com/watch?v=",
            "https://www.youtube.com/embed/")
        lesson = {
            "course_name": request.form.get("course_name"),
            "course_module": request.form.get("course_module"),
            "lesson_title": request.form.get("lesson_title"),
            "lesson_nr": request.form.get("lesson_nr"),
            "lesson_description": request.form.get("lesson_description"),
            "due_date": request.form.get("due_date"),
            "is_mandatory": is_mandatory,
            "has_audio": has_audio,
            "lesson_audio": request.form.get("lesson_audio"),
            "has_video": has_video,
            "lesson_video": lesson_video,
            "has_submission": has_submission,
            "lesson_test": request.form.get("lesson_test"),
            "text_answer": text_answer,
            "file_answer": file_answer,
            "created_by": session["user"]
        }
        mongo.db.lessons.insert_one(lesson)
        flash("Lesson is Added")
    # check if user is a teacher
    allow_role = ["teacher", "admin"]
    if session.get("role") in allow_role:
        # what courses are assigned
        course = session.get("course").capitalize()
        return render_template("add_lesson.html", course=course)

    else:
        # if user is a somebody else
        flash("To become a Teacher, one must first study hard")
        # not allowed
        return redirect(url_for("login"))


@app.route("/edit_lesson/<lesson_id>", methods=["POST", "GET"])
def edit_lesson(lesson_id):
    if request.method == "POST":
        is_mandatory = "on" if request.form.get("is_mandatory") else "off"
        has_audio = "on" if request.form.get("has_audio") else "off"
        has_video = "on" if request.form.get("has_video") else "off"
        has_submission = "on" if request.form.get("has_submission") else "off"
        text_answer = "on" if request.form.get("text_answer") else "off"
        file_answer = "on" if request.form.get("file_answer") else "off"
        lesson_video = request.form.get("lesson_video").replace(
            "https://www.youtube.com/watch?v=",
            "https://www.youtube.com/embed/")
        edit = {
            "course_name": request.form.get("course_name"),
            "course_module": request.form.get("course_module"),
            "lesson_title": request.form.get("lesson_title"),
            "lesson_nr": request.form.get("lesson_nr"),
            "lesson_description": request.form.get("lesson_description"),
            "due_date": request.form.get("due_date"),
            "is_mandatory": is_mandatory,
            "has_audio": has_audio,
            "lesson_audio": request.form.get("lesson_audio"),
            "has_video": has_video,
            "lesson_video": lesson_video,
            "has_submission": has_submission,
            "lesson_test": request.form.get("lesson_test"),
            "text_answer": text_answer,
            "file_answer": file_answer,
            "created_by": session["user"]
        }
        mongo.db.lessons.update({"_id": ObjectId(lesson_id)}, edit)
        flash("Lesson is now updated")

    lesson = mongo.db.lessons.find_one({"_id": ObjectId(lesson_id)})
    lessons = list(mongo.db.lessons.find())
    course = session.get("course").capitalize()
    user = session.get("user")
    # check if user is a teacher
    allow_role = ["teacher", "admin"]
    if session.get("role") in allow_role:
        # what courses are assigned
        course = session.get("course").capitalize()
        # who created the course
        created = lesson.get("created_by")
        if created in user:
            # Only the teacher who created the lesson has access
            return render_template(
                "edit_lesson.html", lesson=lesson,
                course=course, lessons=lessons)

        else:
            # if teacher is not the creator
            flash("Oops, you can only edit your own lessons")
            # not allowed
            return redirect(url_for("login"))

    else:
        # if user is not a teacher or admin
        flash("To become a Teacher, one must first study hard")
        # not allowed
        return redirect(url_for("login"))


@app.route("/edit_user/<user_id>", methods=["POST", "GET"])
def edit_user(user_id):
    if request.method == "POST":
        edit = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "role": request.form.get("role"),
            "assigned_course": request.form.get("assigned_course"),
            "enrollment_day": request.form.get("enrollment_day"),
            "status": request.form.get("status")
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, edit)
        flash("User is now updated")

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    users = list(mongo.db.users.find())
    courses = list(mongo.db.courses.find())
    # check if user is a admin
    if session.get("role") == "admin":
        return render_template(
            "edit_user.html", user=user, users=users, courses=courses)

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("login"))


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    # check if user is a admin
    if session.get("role") == "admin":
        flash("User deleted")
        return redirect(url_for("get_users"))

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("login"))


@app.route("/delete_lesson/<lesson_id>")
def delete_lesson(lesson_id):
    mongo.db.lessons.remove({"_id": ObjectId(lesson_id)})
    # check if user is a admin
    if session.get("role") == "teacher":
        flash("Lesson deleted")
        return redirect(url_for("get_lessons"))

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
