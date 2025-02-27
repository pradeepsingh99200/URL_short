import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Add parent directory to path

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import random
import string
from config import Config  # Now it should work

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.config.from_object(Config)

app.secret_key = os.environ.get("SECRET_KEY", "b7c3f8d1e6a2f9g5h4j0k7l3m2n9p6q8")
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        return conn
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            original_url = request.form.get("url")
            if original_url:
                conn = get_db_connection()
                if not conn:
                    flash("Database connection failed!", "danger")
                    return render_template("index.html")

                cursor = conn.cursor()
                short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

                cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (%s, %s)", (original_url, short_code))
                conn.commit()
                cursor.close()
                conn.close()

                return render_template("short_url.html", short_code=short_code)

        return render_template("index.html")
    except Exception as e:
        print(f"Error in index route: {str(e)}")
        return f"Internal Server Error: {str(e)}", 500
    

@app.route("/<short_code>")
def redirect_to_url(short_code):
    try:
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed!", "danger")
            return redirect(url_for("index"))

        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_code = %s", (short_code,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if result:
            return redirect(result[0])  # Redirect to the original URL
        else:
            flash("Short URL not found!", "danger")
            return redirect(url_for("index"))
    
    except Exception as e:
        print(f"Error in redirect route: {e}")
        return f"Internal Server Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
