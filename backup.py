from flask import Flask, request, render_template_string
import os
import shutil
from datetime import datetime

app = Flask(__name__)

# HTML template for the form and output
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Backup Files</title>
</head>
<body>
    <h1>File Backup Tool</h1>
    <form method="POST">
        <label>Source Directory:</label><br>
        <input type="text" name="source_dir" size="50" required><br><br>
        <label>Destination Directory:</label><br>
        <input type="text" name="dest_dir" size="50" required><br><br>
        <input type="submit" value="Start Backup">
    </form>
    <hr>
    {% if log %}
        <h2>Backup Log:</h2>
        <pre>{{ log }}</pre>
    {% endif %}
</body>
</html>
"""

def backup_files(source_dir, dest_dir):
    log_messages = []

    # Check if source directory exists
    if not os.path.exists(source_dir):
        log_messages.append(f"Error: Source directory '{source_dir}' does not exist.")
        return log_messages

    # Check/create destination directory
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            log_messages.append(f"Created destination directory '{dest_dir}'.")
        except Exception as e:
            log_messages.append(f"Error creating destination directory: {e}")
            return log_messages

    # Loop through files in source
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        if os.path.isfile(source_file):
            dest_file = os.path.join(dest_dir, filename)

            # Append timestamp if file exists
            if os.path.exists(dest_file):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                name, ext = os.path.splitext(filename)
                dest_file = os.path.join(dest_dir, f"{name}_{timestamp}{ext}")

            try:
                shutil.copy2(source_file, dest_file)
                log_messages.append(f"Backed up '{filename}' -> '{dest_file}'")
            except Exception as e:
                log_messages.append(f"Error copying '{filename}': {e}")

    return log_messages

@app.route("/", methods=["GET", "POST"])
def home():
    log = None
    if request.method == "POST":
        source_dir = request.form.get("source_dir")
        dest_dir = request.form.get("dest_dir")
        log = "\n".join(backup_files(source_dir, dest_dir))
    return render_template_string(HTML_TEMPLATE, log=log)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
