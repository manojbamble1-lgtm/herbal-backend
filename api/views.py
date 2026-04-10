import requests
import base64

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import User, Remedy, HerbProfile


# =========================
# REGISTER USER
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=400)

    user = User.objects.create(
        name=request.data.get('name', ""),
        age=request.data.get('age', 0),
        email=email,
        allergies=request.data.get('allergies', ""),
        body_type=request.data.get('body_type', ""),
        password=make_password(password)
    )

    return Response({
        "message": "User Registered Successfully",
        "user_id": user.id
    }, status=201)


# =========================
# LOGIN USER
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    try:
        user = User.objects.get(email=email)

        if check_password(password, user.password):
            return Response({
                "message": "Login Successful",
                "user_id": user.id,
                "name": user.name or "User"
            })

        return Response({"error": "Invalid Email or Password"}, status=401)

    except User.DoesNotExist:
        return Response({"error": "Invalid Email or Password"}, status=401)


# =========================
# PROFILE
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def get_user_profile(request):
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({"error": "User ID required"}, status=400)

    try:
        user = User.objects.get(id=user_id)

        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "allergies": user.allergies,
            "body_type": user.body_type,
        })

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# =========================
# REMEDY
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def get_remedy(request):
    symptom = request.data.get('symptom')

    if not symptom:
        return Response({"error": "Symptom required"}, status=400)

    remedies = Remedy.objects.filter(symptoms__icontains=symptom)

    result = [
        {"title": r.title, "preparation": r.preparation}
        for r in remedies
    ]

    return Response(result)


# =========================
# HEALTH SCORE
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def health_score(request):
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({"error": "User ID required"}, status=400)

    try:
        user = User.objects.get(id=user_id)

        score = 100
        age = int(user.age) if user.age else 0

        if age > 60:
            score -= 20
        elif age > 40:
            score -= 10

        if user.allergies:
            score -= 10

        status_text = (
            "Good" if score >= 80 else
            "Moderate" if score >= 50 else
            "Poor"
        )

        return Response({
            "health_score": score,
            "status": status_text
        })

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# =========================
# AI CHAT
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def ai_chat(request):
    message = request.data.get('message')

    if not message:
        return Response({"error": "Message required"}, status=400)

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": message}]
            }
        )

        data = res.json()
        reply = data.get('choices', [{}])[0].get('message', {}).get('content', '')

        return Response({"reply": reply})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# =========================
# IMAGE SCAN (UPDATED FOR DETAILS)
# =========================
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def scan_herb_ai(request):
    image = request.FILES.get('image')

    if not image:
        return Response({"error": "Image required"}, status=400)

    try:
        image_base64 = base64.b64encode(image.read()).decode()

        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/auto",
                "messages": [{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Identify this herb and give details like name, benefits, uses and precautions"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }]
            }
        )

        data = res.json()
        result = data.get('choices', [{}])[0].get('message', {}).get('content', '')

        return Response({"result": result})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# =========================
# 💚 EMOTION AI
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def emotion_ai(request):
    message = request.data.get('message')

    if not message:
        return Response({"error": "Message required"}, status=400)

    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": message}]
            }
        )

        data = res.json()
        result = data.get('choices', [{}])[0].get('message', {}).get('content', '')

        return Response({"result": result})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# =========================
# 🧬 HERB DNA ENGINE (UPDATED SMART SCORING)
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def herb_dna_engine(request):
    user_id = request.data.get('user_id')
    symptom = request.data.get('symptom')

    if not user_id or not symptom:
        return Response({"error": "user_id and symptom required"}, status=400)

    try:
        user = User.objects.get(id=user_id)

        prompt = f"""
User details:
Age: {user.age}
Body type: {user.body_type}
Allergies: {user.allergies}

Symptom: {symptom}

Give herbal remedies.
"""

        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data = res.json()
        ai_text = data.get('choices', [{}])[0].get('message', {}).get('content', '')

        # 🔥 NEW SMART HERB DATA
        herbs = [
            {"name": "Ashwagandha", "type": "Vata"},
            {"name": "Turmeric", "type": "Pitta"},
            {"name": "Neem", "type": "Kapha"},
        ]

        result = []

        for herb_data in herbs:
            herb = herb_data["name"]
            herb_type = herb_data["type"]

            score = 100

            # ❌ Allergy penalty
            if user.allergies and herb.lower() in user.allergies.lower():
                score -= 40

            # 👴 Age factor
            if user.age:
                age = int(user.age)
                if age > 60:
                    score -= 20
                elif age > 40:
                    score -= 10

            # 🧬 Body type compatibility
            if user.body_type:
                if user.body_type.lower() == herb_type.lower():
                    score += 10
                else:
                    score -= 10

            # 🤒 Symptom relevance
            if symptom.lower() in ["stress", "anxiety"]:
                if herb == "Ashwagandha":
                    score += 20
                else:
                    score -= 5

            if symptom.lower() in ["cold", "cough"]:
                if herb == "Turmeric":
                    score += 20

            # 🔁 Feedback learning
            profile, _ = HerbProfile.objects.get_or_create(
                user=user,
                herb_name=herb
            )

            score += profile.feedback

            # ⚠️ Limit score between 0–100
            score = max(0, min(score, 100))

            profile.score = score
            profile.save()

            result.append({
                "herb": herb,
                "score": score
            })

        return Response({
            "ai_recommendation": ai_text,
            "compatibility": result
        })

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# =========================
# 🔁 FEEDBACK SYSTEM
# =========================
@api_view(['POST'])
@parser_classes([JSONParser])
def herb_feedback(request):
    user_id = request.data.get('user_id')
    herb = request.data.get('herb')
    feedback = int(request.data.get('feedback', 0))

    try:
        profile = HerbProfile.objects.get(user_id=user_id, herb_name=herb)
        profile.feedback += feedback
        profile.save()

        return Response({"message": "Feedback updated"})

    except HerbProfile.DoesNotExist:
        return Response({"error": "Herb not found"}, status=404)