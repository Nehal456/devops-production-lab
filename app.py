from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Count the HTTP requests received by the application.
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"]
)

# Measure how long requests take to process.
REQUEST_LATENCY = Histogram(
    "app_request_duration_seconds",
    "HTTP requests processing time in seconds",
    ["endpoint"]
)

@app.before_request
def start_timer():
    from flask import request
    import time

    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    from flask import request
    import time

    duration = time.time() - getattr(request, "start_time", time.time())

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or "unknown",
        http_status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.endpoint or "unknown"
    ).observe(duration)

    return response

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/version")
def version():
    return jsonify({"version": "1.0.0"})

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)