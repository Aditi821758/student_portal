from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "student_portal_secret_key"

STUDENTS = {
    "student1": {
        "name": "Ava Johnson",
        "email": "ava.johnson@studentportal.edu",
        "major": "Computer Science",
        "year": "2nd Year"
    }
}

COURSES = [
    {"code": "CS101", "title": "Intro to Programming", "instructor": "Dr. Lee", "credits": 3},
    {"code": "MATH210", "title": "Discrete Mathematics", "instructor": "Prof. Kumar", "credits": 4},
    {"code": "ENG205", "title": "Technical Writing", "instructor": "Ms. Brown", "credits": 2},
]

GRADES = {
    "CS101": {"assignment1": 92, "midterm": 88, "final": 94},
    "MATH210": {"quiz1": 85, "assignment1": 90, "midterm": 82},
    "ENG205": {"essay1": 95, "presentation": 89, "portfolio": 91},
}

ASSIGNMENTS = [
    {"title": "Python Lab 1", "course": "CS101", "due": "2026-10-12", "status": "Submitted"},
    {"title": "Logic Worksheet", "course": "MATH210", "due": "2026-10-15", "status": "Pending"},
    {"title": "Research Summary", "course": "ENG205", "due": "2026-10-18", "status": "In Progress"},
]

def login_required(view_func):
    def wrapper(*args, **kwargs):
        if "student_id" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background: #f3f6fb;
            color: #1f2937;
        }
        .container {
            max-width: 1000px;
            margin: 30px auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 10px;
        }
        nav a {
            margin-right: 15px;
            text-decoration: none;
            color: #2563eb;
            font-weight: bold;
        }
        .card {
            background: #f8fafc;
            padding: 18px;
            border-radius: 10px;
            margin-top: 15px;
            border: 1px solid #e2e8f0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #e5e7eb;
        }
        th {
            background: #eef2ff;
        }
        form {
            display: flex;
            flex-direction: column;
            max-width: 350px;
            gap: 10px;
        }
        input, button {
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }
        .logout {
            color: #dc2626;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="topbar">
            <h2>{{ title }}</h2>
            {% if student %}
            <nav>
                <a href="{{ url_for('dashboard') }}">Dashboard</a>
                <a href="{{ url_for('courses') }}">Courses</a>
                <a href="{{ url_for('grades') }}">Grades</a>
                <a href="{{ url_for('assignments') }}">Assignments</a>
                <a class="logout" href="{{ url_for('logout') }}">Logout</a>
            </nav>
            {% endif %}
        </div>

        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    if "student_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        if student_id in STUDENTS:
            session["student_id"] = student_id
            return redirect(url_for("dashboard"))
        return render_template_string(HTML_TEMPLATE, title="Student Portal", student=None) + """
        <div class='card'>
            <p style='color:red;'>Invalid student ID. Try: student1</p>
            <form method='POST'>
                <input type='text' name='student_id' placeholder='Enter Student ID' required>
                <button type='submit'>Login</button>
            </form>
        </div>
        """
    return render_template_string(HTML_TEMPLATE, title="Student Portal", student=None) + """
    <div class='card'>
        <form method='POST'>
            <input type='text' name='student_id' placeholder='Enter Student ID' required>
            <button type='submit'>Login</button>
        </form>
    </div>
    """

@app.route("/dashboard")
@login_required
def dashboard():
    student_id = session["student_id"]
    student = STUDENTS[student_id]
    return render_template_string(HTML_TEMPLATE, title="Dashboard", student=student) + """
    <div class='card'>
        <h3>Welcome, {{ student['name'] }}</h3>
        <p><strong>Email:</strong> {{ student['email'] }}</p>
        <p><strong>Major:</strong> {{ student['major'] }}</p>
        <p><strong>Year:</strong> {{ student['year'] }}</p>
    </div>
    <div class='card'>
        <h3>Quick Summary</h3>
        <p>Total Courses: 3</p>
        <p>Current GPA: 3.9</p>
        <p>Upcoming Deadlines: 2</p>
    </div>
    """, student=student

@app.route("/courses")
@login_required
def courses():
    student_id = session["student_id"]
    student = STUDENTS[student_id]
    return render_template_string(HTML_TEMPLATE, title="Courses", student=student) + """
    <div class='card'>
        <table>
            <tr>
                <th>Code</th>
                <th>Course</th>
                <th>Instructor</th>
                <th>Credits</th>
            </tr>
            {% for course in courses %}
            <tr>
                <td>{{ course['code'] }}</td>
                <td>{{ course['title'] }}</td>
                <td>{{ course['instructor'] }}</td>
                <td>{{ course['credits'] }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    """, courses=COURSES

@app.route("/grades")
@login_required
def grades():
    student_id = session["student_id"]
    student = STUDENTS[student_id]
    return render_template_string(HTML_TEMPLATE, title="Grades", student=student) + """
    <div class='card'>
        <table>
            <tr>
                <th>Course</th>
                <th>Assessment</th>
                <th>Grade</th>
            </tr>
            {% for course, assessments in grades.items() %}
                {% for assessment, score in assessments.items() %}
                <tr>
                    <td>{{ course }}</td>
                    <td>{{ assessment }}</td>
                    <td>{{ score }}%</td>
                </tr>
                {% endfor %}
            {% endfor %}
        </table>
    </div>
    """, grades=GRADES

@app.route("/assignments")
@login_required
def assignments():
    student_id = session["student_id"]
    student = STUDENTS[student_id]
    return render_template_string(HTML_TEMPLATE, title="Assignments", student=student) + """
    <div class='card'>
        <table>
            <tr>
                <th>Title</th>
                <th>Course</th>
                <th>Due Date</th>
                <th>Status</th>
            </tr>
            {% for assignment in assignments %}
            <tr>
                <td>{{ assignment['title'] }}</td>
                <td>{{ assignment['course'] }}</td>
                <td>{{ assignment['due'] }}</td>
                <td>{{ assignment['status'] }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
    """, assignments=ASSIGNMENTS

@app.route("/logout")
def logout():
    session.pop("student_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)