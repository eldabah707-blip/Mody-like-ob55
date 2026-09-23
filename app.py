from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Change this URL if your real Like API is different.
LIKE_API_URL = os.getenv("LIKE_API_URL", "http://br-raja-info-v3.vercel.app/accinfo")

REGIONS = {
    "ME": "الشرق الأوسط",
    "IND": "الهند",
    "ID": "إندونيسيا",
    "SG": "سنغافورة",
    "MY": "ماليزيا",
    "PH": "الفلبين",
    "BD": "بنغلاديش",
}

@app.get("/")
def home():
    return render_template("index.html", regions=REGIONS)

@app.get("/api/player")
def player():
    uid = request.args.get("uid", "").strip()
    region = request.args.get("region", "").strip().lower()
    if not uid:
        return jsonify(ok=False, error="أدخل UID اللاعب"), 400
    if region not in {x.lower() for x in REGIONS}:
        return jsonify(ok=False, error="المنطقة غير مدعومة"), 400

    try:
        r = requests.get(LIKE_API_URL, params={"uid": uid, "region": region}, timeout=10)
        r.raise_for_status()
        data = r.json()
        basic = data.get("basicInfo", {})
        return jsonify(
            ok=True,
            nickname=basic.get("nickname", "Unknown"),
            uid=uid,
            region=region.upper(),
            likes=basic.get("liked", 0),
        )
    except requests.RequestException as e:
        return jsonify(ok=False, error=f"فشل الاتصال بالـ API: {e}"), 502
    except ValueError:
        return jsonify(ok=False, error="الـ API أعاد بيانات غير صالحة"), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
