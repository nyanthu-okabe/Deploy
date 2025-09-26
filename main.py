from flask import Flask, request, render_template, redirect, url_for, flash
import os
import subprocess

app = Flask(__name__)
app.secret_key = "secret"  # flash用
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    files = os.listdir(UPLOAD_FOLDER)
    if request.method == "POST":
        filename = request.form.get("filename", "user.php")
        code = request.form.get("user_input", "")
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        # 保存
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        flash(f"{filename} を保存したで！")
        return redirect(url_for("index"))

    return render_template("index.html", files=files)


@app.route("/run/<filename>")
def run_php(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return "ファイルないで", 404
    try:
        output = subprocess.check_output(["php", filepath], stderr=subprocess.STDOUT)
        return f"<pre>{output.decode('utf-8')}</pre>"
    except subprocess.CalledProcessError as e:
        return f"<pre>エラー:\n{e.output.decode('utf-8')}</pre>"


@app.route("/delete/<filename>")
def delete_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"{filename} を消したで！")
    return redirect(url_for("index"))


@app.route("/load/<filename>")
def load_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return "ファイルないで", 404
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return render_template(
        "index.html",
        files=os.listdir(UPLOAD_FOLDER),
        load_filename=filename,
        load_content=content,
    )


if __name__ == "__main__":
    app.run(debug=True)
