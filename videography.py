# Interactive Videography Guide

# Define emotions and mappings for recommendations
emotions = ["power", "vulnerability", "joy", "sadness", "fear", "surprise", "mystery", "romance", "action", "calm", "other"]

# Camera angle recommendations based on emotion
angle_map = {
    "power": "Low angle",
    "vulnerability": "High angle",
    "joy": "Eye level or slightly low angle",
    "sadness": "High angle or Dutch angle",
    "fear": "High angle or Dutch angle",
    "surprise": "Varies, often extreme close-up or wide shot",
    "mystery": "Low angle or Dutch angle",
    "romance": "Eye level or slightly low angle",
    "action": "Dynamic angles, often following the action",
    "calm": "Eye level or wide angle",
    "other": "Depends on the specific emotion"
}

# Camera movement recommendations based on emotion
movement_map = {
    "power": "Static or slow pan",
    "vulnerability": "Handheld or shaky movement",
    "joy": "Smooth, flowing movement (panning or tracking)",
    "sadness": "Slow, mournful pan or tilt",
    "fear": "Handheld, shaky cam, or quick pans",
    "surprise": "Sudden movements or cuts",
    "mystery": "Slow, suspenseful movement, or tracking shots",
    "romance": "Smooth, romantic tracking or panning",
    "action": "Fast, dynamic movements (tracking, crane shots)",
    "calm": "Static or very slow movement",
    "other": "Depends on the specific emotion"
}

# Composition recommendations based on emotion
composition_map = {
    "power": "Centered composition or rule of thirds with subject dominant",
    "vulnerability": "Off-center, with negative space to emphasize isolation",
    "joy": "Bright, colorful composition, possibly with leading lines to the subject",
    "sadness": "Muted colors, possibly tight framing or isolated subject",
    "fear": "Unbalanced composition, possibly with subjects in corners or tight spaces",
    "surprise": "Composition that leads to the surprise element, often with sudden changes",
    "mystery": "Use of shadows, partially hidden subjects, or leading lines to the unknown",
    "romance": "Soft, intimate composition, often with subjects close together",
    "action": "Dynamic composition with subjects in motion, possibly wide shots",
    "calm": "Balanced, symmetrical composition, often with natural elements",
    "other": "Depends on the specific emotion"
}

# Lighting recommendations based on emotion
lighting_map = {
    "power": "High contrast lighting, strong key light from above or behind",
    "vulnerability": "Soft, low-key lighting, possibly with backlighting",
    "joy": "Bright, natural lighting, warm tones",
    "sadness": "Dim, blue or gray tones, low contrast",
    "fear": "Low-key lighting, harsh shadows, possibly flickering lights",
    "surprise": "Sudden changes in lighting, or flashes of light",
    "mystery": "Low-light, spotlights, or chiaroscuro effect",
    "romance": "Soft, warm lighting, possibly with candles or sunset",
    "action": "High contrast, dynamic lighting to highlight movement",
    "calm": "Soft, even lighting, possibly golden hour for outdoors",
    "other": "Depends on the specific emotion"
}

# Shot duration recommendations based on pace
duration_map = {
    "fast": "Short shots, quick cuts",
    "medium": "Medium duration shots",
    "slow": "Long shots, lingering on the scene"
}

# Welcome message
print("Welcome to the Interactive Videography Guide!")
print("This guide will help you decide on camera angle, movement, composition, lighting, and shot duration based on what you want to convey.")

# Collect user inputs
## Main subject
subject = input("What is the main subject of the shot? (e.g., person, object, landscape): ").strip().lower()

## Emotion selection
print("\nSelect the emotion or feeling you want to convey:")
for i, emotion in enumerate(emotions, 1):
    print(f"{i}. {emotion.capitalize()}")
emotion_choice = input("Enter the number corresponding to your choice: ")
try:
    emotion_index = int(emotion_choice) - 1
    if 0 <= emotion_index < len(emotions):
        emotion = emotions[emotion_index]
    else:
        print("Invalid choice, defaulting to 'other'")
        emotion = "other"
except ValueError:
    print("Invalid input, defaulting to 'other'")
    emotion = "other"

if emotion == "other":
    emotion_desc = input("Please briefly describe the emotion or feeling: ").strip()
else:
    emotion_desc = emotion

## Setting
setting = input("\nIs the setting indoors or outdoors? (or specify a specific location): ").strip().lower()

## Action
action_input = input("\nIs there specific action or movement in the scene? (y/n): ").strip().lower()
if action_input == "y":
    action = input("Please briefly describe the action: ").strip().lower()
else:
    action = None

## Pace selection
print("\nWhat is the desired pace of the scene?")
paces = ["fast", "medium", "slow"]
for i, pace in enumerate(paces, 1):
    print(f"{i}. {pace.capitalize()}")
pace_choice = input("Enter the number corresponding to your choice: ")
try:
    pace_index = int(pace_choice) - 1
    if 0 <= pace_index < len(paces):
        pace = paces[pace_index]
    else:
        print("Invalid choice, defaulting to 'medium'")
        pace = "medium"
except ValueError:
    print("Invalid input, defaulting to 'medium'")
    pace = "medium"

# Generate recommendations based on inputs
## Camera Angle
angle = angle_map.get(emotion, "Choose an angle that best represents the emotion")

## Camera Movement
movement = movement_map.get(emotion, "Choose movement that suits the scene")
if action:
    if "run" in action:
        movement = "Tracking shot to follow the running"
    elif "walk" in action:
        movement = "Tracking shot or panning to follow the walking"
    elif "talk" in action:
        movement = "Static shot or slow pan to focus on the conversation"
    # Additional action-specific adjustments can be added here

## Composition
composition = composition_map.get(emotion, "Choose composition that enhances the emotion")
if subject == "landscape":
    composition += ", use a wide shot to capture the scenery"
elif subject == "person":
    composition += ", focus on the person's face or actions"
elif subject == "object":
    composition += ", highlight the object with appropriate framing"

## Lighting
lighting = lighting_map.get(emotion, "Choose lighting that matches the mood")
if setting == "outdoors":
    lighting += ", utilize natural light, consider the time of day"
elif setting == "indoors":
    lighting += ", use controlled lighting, consider artificial sources"

## Shot Duration
duration = duration_map.get(pace, "Adjust shot duration to match the pace")
if emotion == "surprise":
    duration = "Very short shots or sudden cuts"
elif emotion == "fear" and pace == "slow":
    duration = "Longer shots to build suspense"

# Display recommendations
print("\nBased on your inputs, here are the recommended shot techniques:")
print(f"- **Camera Angle**: {angle}")
print(f"- **Camera Movement**: {movement}")
print(f"- **Composition**: {composition}")
print(f"- **Lighting**: {lighting}")
print(f"- **Shot Duration**: {duration}")

# General advice
print("\n**Note**: These are guidelines. Feel free to experiment and adjust based on your creative vision.")
print("Consider the specific context and how these elements work together to convey your intended message.")