from flask import Flask, request, redirect, url_for, render_template_string
import calendar
from datetime import datetime
import json
import os

app = Flask(__name__)
REMINDERS_FILE = "reminders.json"

# Load and save reminders
def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f)

@app.route("/")
def index():
    year = int(request.args.get("year", datetime.today().year))
    month = int(request.args.get("month", datetime.today().month))
    
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    reminders = load_reminders()

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>{{ month_name }} {{ year }}</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f7f9fc;
            color: #333;
            text-align: center;
            padding: 20px;
        }

        h1 {
            margin-bottom: 10px;
        }

        .nav {
            margin-bottom: 20px;
        }

        .nav a {
            text-decoration: none;
            margin: 0 10px;
            font-weight: bold;
            color: #3b82f6;
        }

        table {
            margin: auto;
            border-collapse: collapse;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }

        th, td {
            padding: 15px;
            border: 1px solid #ddd;
            width: 120px;
            height: 100px;
            background: #fff;
            vertical-align: top;
            border-radius: 8px;
        }

        th {
            background-color: #e0ecff;
            font-weight: bold;
        }

        td {
            position: relative;
            transition: background-color 0.3s;
        }

        td:hover {
            background-color: #f0f8ff;
        }

        .date {
            font-weight: bold;
            font-size: 16px;
        }

        .reminder {
            margin-top: 5px;
            font-size: 14px;
            color: #16a34a;
            text-align: left;
        }

        input[type="text"] {
            width: 90%;
            padding: 4px;
            font-size: 12px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-top: 5px;
        }

        button {
            margin-top: 4px;
            padding: 4px 10px;
            font-size: 12px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #2563eb;
        }
    </style>
</head>
<body>
    <h1>{{ month_name }} {{ year }}</h1>
    <div class="nav">
        <a href="/?year={{ year if month > 1 else year - 1 }}&month={{ month - 1 if month > 1 else 12 }}">← Prev</a>
        <a href="/?year={{ year if month < 12 else year + 1 }}&month={{ month + 1 if month < 12 else 1 }}">Next →</a>
    </div>

    <table>
        <tr>
            {% for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"] %}
                <th>{{ day }}</th>
            {% endfor %}
        </tr>
        {% for week in cal %}
            <tr>
                {% for day in week %}
                    <td>
                        {% if day != 0 %}
                            <div class="date">{{ day }}</div>
                            {% set date_str = "%04d-%02d-%02d" | format(year, month, day) %}
                            {% if date_str in reminders %}
                                <div class="reminder">📌 {{ reminders[date_str] }}</div>
                            {% endif %}
                            <form method="POST" action="/reminder">
                                <input type="hidden" name="date" value="{{ date_str }}">
                                <input type="text" name="reminder" placeholder="Reminder">
                                <button type="submit">Save</button>
                            </form>
                        {% endif %}
                    </td>
                {% endfor %}
            </tr>
        {% endfor %}
    </table>
</body>
</html>
""", year=year, month=month, month_name=month_name, cal=cal, reminders=reminders)

@app.route("/reminder", methods=["POST"])
def reminder():
    date = request.form["date"]
    text = request.form["reminder"].strip()
    
    reminders = load_reminders()
    if text:
        reminders[date] = text
    elif date in reminders:
        del reminders[date]
    
    save_reminders(reminders)
    return redirect(url_for("index", year=date.split("-")[0], month=date.split("-")[1]))

if __name__ == "__main__":
    app.run(debug=True)