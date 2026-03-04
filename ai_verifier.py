import easyocr
from PIL import Image
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

CERT_KEYWORDS = [
"certificate",
"participation",
"achievement",
"award",
"completion"
]

EVENT_KEYWORDS = {
"Hackathon":["hackathon","coding","challenge"],
"Certification":["certificate","course","training"],
"Sports":["tournament","championship","sports"],
"Research":["conference","journal","research","paper"],
"Club":["club","society","event"]
}

def verify_certificate(path, student_name, category):

    try:

        results = reader.readtext(path)

        text = " ".join([r[1] for r in results]).lower()

        score = 0

        # certificate keyword check
        if any(k in text for k in CERT_KEYWORDS):
            score += 0.3

        # name check
        if student_name.lower() in text:
            score += 0.3
            name_match = True
        else:
            name_match = False

        # event keyword check
        if category in EVENT_KEYWORDS:
            if any(k in text for k in EVENT_KEYWORDS[category]):
                score += 0.2

        # text density check
        if len(text) > 50:
            score += 0.1

        # tamper detection
        img = Image.open(path)
        arr = np.array(img)

        variance = np.var(arr)

        tamper = variance > 9500

        if not tamper:
            score += 0.1

        score = round(min(score,1.0),2)

        return {
            "confidence":score,
            "name_match":name_match,
            "edited":tamper
        }

    except:

        return {
            "confidence":0.2,
            "name_match":False,
            "edited":True
        }