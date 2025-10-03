from flask import Flask, render_template_string
import psutil
import time
import threading

app = Flask(__name__)

# Threshold for CPU alert
THRESHOLD = 80
# Interval (seconds) to check CPU usage
CHECK_INTERVAL = 2
# Global variable to store latest CPU usage
cpu_usage = 0

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CPU Monitor</title>
    <meta http-equiv="refresh" content="2">  <!-- Refresh every 2 seconds -->
</head>
<body>
    <h1>CPU Usage Monitor</h1>
    <p>Current CPU Usage: {{ cpu_usage }}%</p>
    {% if cpu_usage > threshold %}
        <p style="color:red;"><strong>Alert! CPU usage exceeds threshold!</strong></p>
    {% endif %}
</body>
</html>
"""

# Function to monitor CPU usage in background
def monitor_cpu():
    global cpu_usage
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > THRESHOLD:
                # Log alert to file
                with open("cpu_alerts.log", "a") as f:
                    f.write(f"{time.ctime()}: ALERT! CPU usage {cpu_usage}% exceeds threshold {THRESHOLD}%\n")
        except Exception as e:
            print(f"Error monitoring CPU: {e}")
        time.sleep(CHECK_INTERVAL - 1)  # Adjust because cpu_percent already waits 1 second

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, cpu_usage=cpu_usage, threshold=THRESHOLD)

if __name__ == "__main__":
    # Start CPU monitoring in a separate thread
    cpu_thread = threading.Thread(target=monitor_cpu)
    cpu_thread.daemon = True
    cpu_thread.start()

    # Run Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)
