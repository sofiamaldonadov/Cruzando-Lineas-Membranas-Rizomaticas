def onValueChange(channel, sampleIndex, val, prev):
    finger_gun_chop = op('finger_gun')  # Ensure this is the correct CHOP name
    detected_chop = op('finger_gun_detected')  # Constant CHOP for output

    if detected_chop is None:
        return  # Skip execution if the CHOP is missing

    # Read finger positions
    thumb_x = finger_gun_chop['h1:thumb_tip:x'][0]  
    thumb_y = finger_gun_chop['h1:thumb_tip:y'][0]  # New: Read thumb Y position
    index_tip_y = finger_gun_chop['h1:index_finger_tip:y'][0]
    index_dip_y = finger_gun_chop['h1:index_finger_dip:y'][0]
    middle_tip_y = finger_gun_chop['h1:middle_finger_tip:y'][0]
    middle_dip_y = finger_gun_chop['h1:middle_finger_dip:y'][0]
    ring_tip_y = finger_gun_chop['h1:ring_finger_tip:y'][0]
    ring_dip_y = finger_gun_chop['h1:ring_finger_dip:y'][0]
    pinky_tip_y = finger_gun_chop['h1:pinky_tip:y'][0]
    pinky_dip_y = finger_gun_chop['h1:pinky_dip:y'][0]

    # **🔧 Adjust these threshold values for better gesture detection**
    UP_THRESHOLD = 0.20  # Fingers are "up" above this Y value
    DOWN_THRESHOLD = 0.20  # Fingers are "down" below this Y value
    THUMB_UP_THRESHOLD = 0.25  # Thumb must be UP (above this Y value)

    # Check finger states
    index_up = index_tip_y > UP_THRESHOLD and index_dip_y > UP_THRESHOLD
    middle_up = middle_tip_y > UP_THRESHOLD and middle_dip_y > UP_THRESHOLD
    ring_down = ring_tip_y < DOWN_THRESHOLD and ring_dip_y < DOWN_THRESHOLD
    pinky_down = pinky_tip_y < DOWN_THRESHOLD and pinky_dip_y < DOWN_THRESHOLD

    # Thumb should be positioned to the side (right of the index finger in x-axis)
    thumb_side = thumb_x > 0.05  # Adjust this based on hand position

    # **Ensure the thumb is UP**
    thumb_up = thumb_y > THUMB_UP_THRESHOLD

    # **Final Condition: Finger Gun Detected**
    detected_chop.par.value0 = 1 if (thumb_side and thumb_up and index_up and middle_up and ring_down and pinky_down) else 0

    return
