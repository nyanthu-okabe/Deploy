from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = "nyanchu_secret"  # セッション用の鍵

# --- 認証設定 ---
USERNAME = "nyanchu"
PASSWORD = "1234"

@app.before_request
def check_login():
    if request.endpoint not in ("login", "static") and not session.get("logged_in"):
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == USERNAME and request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            flash("ユーザ名かパスワードが違います")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

# --- PHPエディタ部分 ---
@app.route("/", methods=["GET", "POST"])
def index():
    load_filename = request.args.get("filename")
    load_content = ""
    files = [f for f in os.listdir("./files") if f.endswith(".php")]

    if request.method == "POST":
        filename = request.form["filename"]
        content = request.form["user_input"]
        with open(f"./files/{filename}", "w", encoding="utf-8") as f:
            f.write(content)
        flash(f"{filename} を保存しました")
        return redirect(url_for("index"))

    if load_filename:
        try:
            with open(f"./files/{load_filename}", "r", encoding="utf-8") as f:
                load_content = f.read()
        except FileNotFoundError:
            flash("ファイルが見つかりません")

    return render_template("index.html", files=files, load_filename=load_filename, load_content=load_content)

if __name__ == "__main__":
    os.makedirs("./files", exist_ok=True)
    app.run(host="0.0.0.0", port=8000, debug=True)
