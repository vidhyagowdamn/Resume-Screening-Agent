from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.pdf_reader import extract_text_from_pdf
from resume_ranker import rank_resume

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Backend running!"


@app.route("/rank", methods=["POST"])
def rank():
    try:
        # files come from FormData key "resume"
        files = request.files.getlist("resume")
        job_desc = request.form.get("job_desc", "")

        results = []

        for file in files:
            text = extract_text_from_pdf(file)
            analysis = rank_resume(text, job_desc)

            results.append({
                "name": file.filename,
                "score": analysis["score"],
                "strengths": analysis["strengths"],
                "gaps": analysis["gaps"],
                "explanation": analysis["explanation"],
                "recommendation": analysis["recommendation"],
            })

        return jsonify(results), 200

    except Exception as e:
        # helps you see errors in terminal if something breaks
        print("Error in /rank:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)