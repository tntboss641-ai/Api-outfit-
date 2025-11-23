from flask import Flask, request, send_file, jsonify
from hammer.outfitgen import outfitgen
import io

app = Flask(__name__)

OWNER = "Lixzyffx"  # اسمك في الـ API


@app.route("/", methods=["GET"])
def home():
    return {
        "api": "Outfit Generator API",
        "author": OWNER,
        "usage": f"/{OWNER}/outfit?id=PLAYER_ID"
    }


@app.route(f"/{OWNER}/outfit", methods=["GET"])
def get_outfit():
    player_id = request.args.get("id")

    if not player_id:
        return jsonify({
            "error": "missing parameter (id)"
        }), 400
    
    try:
        img = outfitgen(player_id)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        return send_file(
            buf,
            mimetype="image/jpeg",
            download_name=f"{player_id}.jpg"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()