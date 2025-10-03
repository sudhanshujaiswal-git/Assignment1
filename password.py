from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# Function to check password strength (with regex)
def check_password_strength(password):
    # Minimum length
    if len(password) < 8:
        return False

    # At least one uppercase
    if not re.search(r"[A-Z]", password):
        return False

    # At least one lowercase
    if not re.search(r"[a-z]", password):
        return False

    # At least one digit
    if not re.search(r"[0-9]", password):
        return False

    # At least one special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True


# Simple HTML page with form
html_form = """
<!doctype html>
<html>
  <head>
    <title>Password Strength Checker</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 50px; }
      input { padding: 8px; margin-right: 10px; }
      button { padding: 8px; }
      h2 { color: #333; }
    </style>
  </head>
  <body>
    <h2> Password Strength Checker</h2>
    <form method="post">
      <input type="password" name="password" placeholder="Enter password" required>
      <button type="submit">Check</button>
    </form>
    {% if result is not none %}
      <h3>{{ result }}</h3>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        password = request.form["password"]
        if check_password_strength(password):
            result = "Strong password!"
        else:
            result = "Weak password. Try including uppercase, lowercase, digit, special character, and at least 8 chars."
    return render_template_string(html_form, result=result)


if __name__ == "__main__":
    # Run Flask app on local IP, port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
