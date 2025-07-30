from flask import Flask, render_template, request, flash
import os
import shutil

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Define file type categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".cpp", ".html", ".css"]
}
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        folder_path = request.form.get("folderPath")
        print(f"Received folder path: {folder_path}")  # Debug

        if not folder_path or not os.path.exists(folder_path):
            flash("❌ Please enter a valid folder path.", "danger")
            return render_template("index.html")

        files = os.listdir(folder_path)
        print(f"Found files: {files}")  # Debug

        count = {}

        for file in files:
            file_path = os.path.join(folder_path, file)
            print(f"Processing file: {file_path}")  # Debug

            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                moved = False

                for category, extensions in FILE_TYPES.items():
                    if ext in extensions:
                        dest_folder = os.path.join(folder_path, category)
                        os.makedirs(dest_folder, exist_ok=True)
                        shutil.move(file_path, os.path.join(dest_folder, file))
                        count[category] = count.get(category, 0) + 1
                        moved = True
                        break

                if not moved:
                    other_folder = os.path.join(folder_path, "Others")
                    os.makedirs(other_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(other_folder, file))
                    count["Others"] = count.get("Others", 0) + 1

        flash("✅ Files organized successfully!", "success")
        for k, v in count.items():
            flash(f"{k}: {v} file(s)", "info")

    return render_template("index2.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
