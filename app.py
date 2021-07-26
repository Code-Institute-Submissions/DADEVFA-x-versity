import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary
import cloudinary.uploader
import cloudinary.api
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# Cloudinary API used to store the item images
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET")
)


@app.route("/")
@app.route("/home")
def home():
    """
    Home route.
    """
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register route. Checks if email already is in use or new.
    Stores username, then sets default role and course in session
    cookies.
    """
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
            "enrollment_day": "pending",
            "apply_course": request.form.get("apply_course")
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


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login route. Stores Username, Role and Course.
    """
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                # store users name, role and course
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


@app.route("/logout")
def logout():
    """
    Logout route. Removes stored session username,
    role and course.
    """
    # remove session cookies
    flash("You have been logged out")
    session.pop("user")
    session.pop("role")
    session.pop("course")
    return redirect(url_for("home"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Profile route. For users to view if they have been
    assigned a course or not.
    """
    # grab the session user's username from cookie
    username = session["user"]
    course = session.get("course")

    if session["user"]:
        return render_template(
            "profile.html", username=username, course=course)

    else:
        return redirect(url_for("login"))


@app.route("/add_lesson", methods=["GET", "POST"])
def add_lesson():
    """
    Add Lesson route. Teacher creates their lessons from here.
    """
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
        return redirect(url_for("home"))


@app.route("/edit_lesson/<lesson_id>", methods=["POST", "GET"])
def edit_lesson(lesson_id):
    """
    Edit Lesson route. Teachers can update their lessons. They
    access it from get lessons template.
    """
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
        return redirect(url_for("home"))


@app.route("/get_lessons")
def get_lessons():
    """
    Lesson route. Like a classroom were students
    go through course and submit their work.
    Teachers can edit their lessons from here too.
    """
    course = session.get("course")
    lessons = list(mongo.db.lessons.find(
        {"$text": {"$search": course}}))
    lessons.reverse()
    if course != "pending":
        return render_template(
            "lessons.html", lessons=lessons)

    elif course:
        flash("You will be assigned to your course soon.")
        return redirect(url_for("home"))


@app.route("/student_submit", methods=["POST", "GET"])
def student_submit():
    """
    Student Submit route. Makes submissions possible,
    both file and text even though they are separate forms.
    """
    if request.method == 'POST':
        files_upload = {}
        if "file_submission" in request.files:
            files = request.files['file_submission']
            files_upload = cloudinary.uploader.upload(files)
            # check if user is a student
        if session.get("role") == "student":
            # get the time and day
            submit_time = datetime.now()
            date = submit_time.strftime("%d/%m/%Y %H:%M:%S")
            submit = {
                "text_submission": request.form.get("text_submission"),
                "file_submission": files_upload["secure_url"] if "secure_url"
                in files_upload else "",
                "student": session["user"],
                "course_name": session["course"],
                "date": date,
                "grade": "",
                "feedback": ""
            }
            mongo.db.submissions.insert_one(submit)
            flash("Your answer has been submitted")
            return redirect(url_for("get_lessons"))

        else:
            # if user is not a student
            flash("Ops, are you sure you´re studing this course?")
            # not allowed
            return redirect(url_for("home"))


@app.route("/submissions")
def get_submits():
    """
    Submissions route. For teachers to view all their students
    submissions, course filter is included in template.
    """
    submissions = list(mongo.db.submissions.find())
    submissions.reverse()
    if session.get("role") == "teacher":
        return render_template("submissions.html", submissions=submissions)

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


@app.route("/grade_submission/<submission_id>", methods=["POST", "GET"])
def grade_submission(submission_id):
    """
    Grade Submissions route. Teachers can assess submissions made by
    their students and then grade it.
    """
    if request.method == "POST":
        # teacher sets grade and gives feedback
        grade = {"$set": {
            "grade": request.form.get("grade"),
            "feedback": request.form.get("feedback")}
            }
        mongo.db.submissions.update({"_id": ObjectId(submission_id)}, grade)
        flash("Submission is has been graded")

    submission = mongo.db.submissions.find_one(
        {"_id": ObjectId(submission_id)})
    submissions = list(mongo.db.submissions.find())
    # check if user is a admin
    if session.get("role") == "teacher":
        return render_template(
            "grade_submission.html", submission=submission,
            submissions=submissions)

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


@app.route("/delete_lesson/<lesson_id>")
def delete_lesson(lesson_id):
    """
    Delete Lessons route. Teachers can delete their lessons.
    """
    mongo.db.lessons.remove({"_id": ObjectId(lesson_id)})
    # check if user is a admin
    if session.get("role") == "teacher":
        flash("Lesson deleted")
        return redirect(url_for("get_lessons"))

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


@app.route("/users")
def get_users():
    """
    Users route. Admin view all registered users
    from here.
    """
    users = list(mongo.db.users.find())
    users.reverse()
    if session.get("role") == "admin":
        return render_template("users.html", users=users)

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


@app.route("/edit_user/<user_id>", methods=["POST", "GET"])
def edit_user(user_id):
    """
    Edit User route. Admin updates users information and also sets
    privileges and courses.
    """
    if request.method == "POST":
        # To prevent password from updating
        password = request.form.get("password")
        if len(password) == 0:
            # Empty means same
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            password = user["password"]
        else:
            # New
            password = generate_password_hash(request.form.get("password"))
        edit = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": password,
            "role": request.form.get("role"),
            "assigned_course": request.form.get("assigned_course"),
            "enrollment_day": request.form.get("enrollment_day"),
            "status": request.form.get("status"),
            "apply_course": request.form.get("apply_course")
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
        return redirect(url_for("home"))


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    """
    Delete User route. Admin can remove users.
    """
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    # check if user is a admin
    if session.get("role") == "admin":
        flash("User deleted")
        return redirect(url_for("get_users"))

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("homev"))


@app.route("/get_courses")
def get_courses():
    """
    Get Courses route. Admin can see all courses.
    """
    # check if user is a admin
    if session.get("role") == "admin":
        courses = list(mongo.db.courses.find().sort("course_name", 1))
        return render_template("courses.html", courses=courses)

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    """
    Add Courses route. Admin can add a new course.
    """
    # check if user is a admin
    if session.get("role") == "admin":
        if request.method == "POST":
            courses = {
                "course_name": request.form.get("course_name")
            }
            mongo.db.courses.insert_one(courses)
            flash("New Course Added")
            return redirect(url_for("get_courses"))
        return render_template("add_course.html")

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


@app.route("/edit_course/<course_id>", methods=["GET", "POST"])
def edit_course(course_id):
    """
    Edit Courses route. Admin can Edit a new course.
    """
    # check if user is a admin
    if session.get("role") == "admin":
        if request.method == "POST":
            edit = {
                "course_name": request.form.get("course_name")
            }
            mongo.db.courses.update({"_id": ObjectId(course_id)}, edit)
            flash("Course is now updated")
            return redirect(url_for("get_courses"))
        course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})
        return render_template("edit_course.html", course=course)

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


@app.route("/delete_course/<course_id>")
def delete_course(course_id):
    """
    Delete Course route. Admin can delete course.
    """
    mongo.db.course.remove({"_id": ObjectId(course_id)})
    # check if user is a admin
    if session.get("role") == "admin":
        flash("Course deleted")
        return redirect(url_for("get_courses"))

    else:
        # session user shouldn't be here
        flash("Ops, something went wrong")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
