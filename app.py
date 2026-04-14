# =============================================================================
# Skill Swap Hub - Flask Application 
# COM4113 Tech Stack - Leeds Trinity University
# =============================================================================


from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

# =============================================================================
# APP CONFIGURATION
# =============================================================================

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"

MONGO_URI = "mongodb+srv://2407581:Robert2804@cluster0.cspwq.mongodb.net/?appName=Cluster0"
DB_NAME = "skillswap_db"

# File upload settings
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =============================================================================
# DATABASE CONNECTION
# =============================================================================

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db["users"]
    resources_collection = db["resources"]
    client.admin.command("ping")
    print("Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    print("Please check your MONGO_URI in app.py")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_logged_in_user():
    """Return the logged-in user's document from the database, or None."""
    if "username" in session:
        try:
            user = users_collection.find_one({"username": session["username"]})
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
    return None


# =============================================================================
# CUSTOM ERROR HANDLERS
# =============================================================================

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error with a custom page."""
    return render_template("error500.html"), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html"), 404


# =============================================================================
# ROUTES
# =============================================================================


# --- Home Page ---------------------------------------------------------------
@app.route("/")
def home():
    """Display the home page."""
    user = get_logged_in_user()
    return render_template("index.html", user=user)


# --- User Registration -------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    GET:  Display the registration form.
    POST: Validate input, hash password, and create user in MongoDB.
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        bio = request.form.get("bio", "").strip()
        hobbies = request.form.get("hobbies", "").strip()

        # Server-side validation for required fields
        if not username or not email or not password:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("register"))

        # Check for duplicate username (was TODO 1 in Sample 00, now complete)
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register"))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Handle profile photo upload
        profile_photo = "uploads/placeholder.png"
        if "profile_photo" in request.files:
            file = request.files["profile_photo"]
            if file and file.filename != "" and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_name))
                profile_photo = f"uploads/{unique_name}"

        user_doc = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "bio": bio,
            "hobbies": hobbies,
            "profile_photo": profile_photo,
            "created_at": datetime.now()
        }

        try:
            users_collection.insert_one(user_doc)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Registration failed: {e}", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


# --- User Login (was TODO 2 in Sample 00, now complete) ----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    GET:  Display the login form.
    POST: Verify credentials and create a session.
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return redirect(url_for("login"))

        try:
            user = users_collection.find_one({"username": username})

            # Completed: password verification and session creation
            if user and check_password_hash(user["password"], password):
                session["username"] = username
                flash("Welcome back!", "success")
                return redirect(url_for("timeline"))
            else:
                flash("Invalid username or password.", "error")
                return redirect(url_for("login"))

        except Exception as e:
            flash(f"Login error: {e}", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


# --- User Logout -------------------------------------------------------------
@app.route("/logout")
def logout():
    """Clear the session and redirect to the home page."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


# --- Skills Timeline with Filtering and Search -------------------------------
@app.route("/timeline")
def timeline():
    """
    Fetch and display resources from MongoDB.
    Supports optional category filtering and keyword search.
    """
    # Get filter and search parameters from the URL query string
    selected_category = request.args.get("category", "")
    search_query = request.args.get("q", "").strip()

    try:
        # Build the MongoDB query based on filters
        query = {}

       
        if selected_category:
            query["category"] = selected_category
        
        if search_query:
            query["$or"] = [
                {"title": {"$regex": search_query, "$options": "i"}},
                {"description" : {"$regex": search_query, "$options": "i"}}
            ]
        # Fetch resources using the query, newest first
        resources = list(
            resources_collection.find(query).sort("created_at", -1)
        )

    except Exception as e:
        flash(f"Could not load resources: {e}", "error")
        resources = []

    user = get_logged_in_user()

    # List of categories for the filter dropdown
    categories = [
        "Programming", "Design", "Music", "Photography",
        "Languages", "Cooking", "Fitness", "AI Tools", "Other"
    ]

    return render_template(
        "timeline.html",
        resources=resources,
        user=user,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query
    )


# --- Like a Resource ---------------------------------------------------------
@app.route("/like/<resource_id>")
def like(resource_id):
    """Increase the like count for a resource."""
    try:
        resources_collection.update_one(
            {"_id": ObjectId(resource_id)},
            {"$inc": {"likes": 1}}
        )
    except Exception as e:
        print(f"Like error: {e}")

    return redirect(url_for("timeline"))
 # --- View Single Resource ----------------------------------------------------
@app.route("/resource/<resource_id>")
def view_resource(resource_id):
    try:
        resource = resources_collection.find_one({"_id": ObjectId(resource_id)})
        if not resource:
            return render_template("error404.html"), 404
    except Exception as e:
        print(f"Resource error: {e}")
        return render_template("error500.html"), 500

    user = get_logged_in_user()
    return render_template("resource.html", resource=resource, user=user)


# --- Post a New Resource (with validation) -----------------------------------
@app.route("/post_resource", methods=["GET", "POST"])
def post_resource():
    """
    GET:  Display the resource submission form.
    POST: Validate input and save the resource to MongoDB.
    """
    user = get_logged_in_user()
    if not user:
        flash("Please log in to share a resource.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        link = request.form.get("link", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()


        
        if not title or not description:
            flash("Title and description are required.", "error")
            return redirect(url_for("post_resource"))
        if len(title) >100:
            flash("Title must be 100 characters or fewer.", "error")
            return redirect(url_for("post_resource"))
        if len(description) < 10:
            flash("Description must be at least 10 characters", "error")
            return redirect(url_for("post_resource"))
        
        resource_doc = {
            "title": title,
            "link": link,
            "description": description,
            "category": category,
            "author": user["username"],
            "author_photo": user.get("profile_photo", "uploads/placeholder.png"),
            "created_at": datetime.now(),
            "likes": 0, 
        }

        try:
            resources_collection.insert_one(resource_doc)
            flash("Resource shared successfully!", "success")
            return redirect(url_for("timeline"))
        except Exception as e:
            flash(f"Could not save resource: {e}", "error")
            return redirect(url_for("post_resource"))

    return render_template("post_resource.html", user=user)


# --- User Profile ------------------------------------------------------------
@app.route("/profile")
def profile():
    """Display the logged-in user's profile and their posted resources."""
    user = get_logged_in_user()
    if not user:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("login"))

    # Fetch resources posted by this user
    try:
        user_resources = list(
            resources_collection.find(
                {"author": user["username"]}
            ).sort("created_at", -1)
        )
    except Exception:
        user_resources = []

    return render_template(
        "profile.html", user=user, user_resources=user_resources
    )


# --- Edit Profile ------------------------------------------------------------
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    """
    GET:  Display the profile edit form.
    POST: Update user details in MongoDB.
    """
    user = get_logged_in_user()
    if not user:
        flash("Please log in to edit your profile.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        new_bio = request.form.get("bio", "").strip()
        new_hobbies = request.form.get("hobbies", "").strip()
        new_email = request.form.get("email", "").strip()

       
        
        profile_photo = user.get("profile_photo", "uploads/placeholder.png")
        if "profile_photo" in request.files:
            file = request.files["profile_photo"]
            if file and file.filename != "" and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_name))
                profile_photo = f"uploads/{unique_name}"

        try:
            users_collection.update_one(
                {"username": session["username"]},
                {"$set": {
                    "email": new_email,
                    "bio": new_bio,
                    "hobbies": new_hobbies,
                    "profile_photo": profile_photo
                }}
            )
            flash("Profile updated successfully!", "success")
            return redirect(url_for("profile"))
        except Exception as e:
            flash(f"Could not update profile: {e}", "error")    

    return render_template("edit_profile.html", user=user)


# =============================================================================
# RUN THE APPLICATION
# =============================================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)