# Detection thresholds
DETECTION_THRESHOLD = 0.02  # Finger detection threshold
THUMB_FOLD_X_THRESHOLD_LEFT = 0.45  # Lower X = Folded for left hand
THUMB_FOLD_X_THRESHOLD_RIGHT = 0.55  # Higher X = Folded for right hand

def onValueChange(channel, sampleIndex, val, prev):
    num4_chop = op('number_4_detected')  # Output CHOP
    hand_chop = op('number_4')  # CHOP containing hand tracking data

    # Ensure `hand_chop` is valid and has data
    if not hand_chop or hand_chop.numChans == 0:
        return

    try:
        # Get Y values for detecting finger positions
        index_tip = float(hand_chop['h1:index_finger_tip:y'][0])
        index_dip = float(hand_chop['h1:index_finger_dip:y'][0])
        middle_tip = float(hand_chop['h1:middle_finger_tip:y'][0])
        middle_dip = float(hand_chop['h1:middle_finger_dip:y'][0])
        ring_tip = float(hand_chop['h1:ring_finger_tip:y'][0])
        ring_dip = float(hand_chop['h1:ring_finger_dip:y'][0])
        pinky_tip = float(hand_chop['h1:pinky_tip:y'][0])
        pinky_dip = float(hand_chop['h1:pinky_dip:y'][0])

        # Get X values for thumb folding
        thumb_tip_x = float(hand_chop['h1:thumb_tip:x'][0])
        thumb_ip_x = float(hand_chop['h1:thumb_ip:x'][0])
        thumb_mcp_x = float(hand_chop['h1:thumb_mcp:x'][0])

    except KeyError:
        return

    # Determine if the hand is left or right based on X positions
    is_right_hand = thumb_tip_x > thumb_mcp_x
    is_left_hand = not is_right_hand  

    # Detect if each finger is up (Tip is significantly higher than DIP)
    index_up = index_tip > (index_dip + DETECTION_THRESHOLD)
    middle_up = middle_tip > (middle_dip + DETECTION_THRESHOLD)
    ring_up = ring_tip > (ring_dip + DETECTION_THRESHOLD)
    pinky_up = pinky_tip > (pinky_dip + DETECTION_THRESHOLD)

    # Determine thumb folded status based on hand orientation
    if is_right_hand:
        thumb_folded = thumb_tip_x > THUMB_FOLD_X_THRESHOLD_RIGHT  
    else:
        thumb_folded = thumb_tip_x < THUMB_FOLD_X_THRESHOLD_LEFT  

    # 4 fingers up, thumb folded condition
    is_four_fingers = index_up and middle_up and ring_up and pinky_up and thumb_folded

    # Update the constant CHOP
    num4_chop.par.value0 = 1 if is_four_fingers else 0

    return
