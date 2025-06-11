def onValueChange(channel, sampleIndex, val, prev):
    finger_chop = op('h1_crossing_fingers')  # Ensure this matches your CHOP name
    detected_chop = op('h1_crossing_fingers_detected')  # Constant CHOP for output

    if detected_chop is None:
        return  # Skip execution if CHOP is missing

    # Read finger positions for the first hand (h1)
    index_tip_x = finger_chop['h1:index_finger_tip:x'][0]
    index_tip_y = finger_chop['h1:index_finger_tip:y'][0]
    middle_tip_x = finger_chop['h1:middle_finger_tip:x'][0]
    middle_tip_y = finger_chop['h1:middle_finger_tip:y'][0]
    ring_tip_y = finger_chop['h1:ring_finger_tip:y'][0]
    pinky_tip_y = finger_chop['h1:pinky_tip:y'][0]
    thumb_tip_y = finger_chop['h1:thumb_tip:y'][0]  # New thumb value

    # **🔧 Adjust these threshold values for better detection**
    UP_THRESHOLD = 0.20  # Fingers "up" if Y is above this value
    DOWN_THRESHOLD = 0.20  # Fingers "down" if Y is below this value
    CROSS_THRESHOLD = 0.06  # Max X distance for index & middle fingers to be crossed
    THUMB_DOWN_THRESHOLD = 0.20  # Thumb must be "down" (below this Y value)

    # Check if index and middle fingers are up
    index_up = index_tip_y > UP_THRESHOLD
    middle_up = middle_tip_y > UP_THRESHOLD

    # Check if ring and pinky fingers are down
    ring_down = ring_tip_y < DOWN_THRESHOLD
    pinky_down = pinky_tip_y < DOWN_THRESHOLD

    # Check if index and middle fingers are close together (crossed)
    fingers_crossed = abs(index_tip_x - middle_tip_x) < CROSS_THRESHOLD

    # Check if thumb is down
    thumb_down = thumb_tip_y < THUMB_DOWN_THRESHOLD

    # **Final Condition: Crossing Fingers Gesture Detected**
    detected_chop.par.value0 = 1 if (index_up and middle_up and fingers_crossed and ring_down and pinky_down and thumb_down) else 0

    return
