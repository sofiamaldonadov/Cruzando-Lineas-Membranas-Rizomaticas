# Detection threshold for finger positions
DETECTION_THRESHOLD = 0.02  # Minimum height difference for "up" detection

def onValueChange(channel, sampleIndex, val, prev):
    # Get CHOP references for second hand
    shaka_chop = op('surfer_h2_detected')  # Output CHOP for detection
    hand_chop = op('surfer_h2')  # CHOP containing second-hand tracking data

    # Ensure `hand_chop` exists and contains data
    if not hand_chop or hand_chop.numChans == 0:
        return  # No valid data, skip processing

    try:
        # Get Y values for finger tip and DIP joints
        index_tip = float(hand_chop['h2:index_finger_tip:y'][0])
        index_dip = float(hand_chop['h2:index_finger_dip:y'][0])
        middle_tip = float(hand_chop['h2:middle_finger_tip:y'][0])
        middle_dip = float(hand_chop['h2:middle_finger_dip:y'][0])
        ring_tip = float(hand_chop['h2:ring_finger_tip:y'][0])
        ring_dip = float(hand_chop['h2:ring_finger_dip:y'][0])
        pinky_tip = float(hand_chop['h2:pinky_tip:y'][0])
        pinky_dip = float(hand_chop['h2:pinky_dip:y'][0])

        # Get X values for thumb folding
        thumb_tip_x = float(hand_chop['h2:thumb_tip:x'][0])
        thumb_ip_x = float(hand_chop['h2:thumb_ip:x'][0])
        thumb_mcp_x = float(hand_chop['h2:thumb_mcp:x'][0])

    except KeyError:
        return  # Some channels missing, skip processing

    # Determine if the hand is left or right based on thumb X position
    is_right_hand = thumb_tip_x > thumb_mcp_x
    is_left_hand = not is_right_hand

    # Detect if middle three fingers are folded
    index_folded = index_tip < (index_dip + DETECTION_THRESHOLD)
    middle_folded = middle_tip < (middle_dip + DETECTION_THRESHOLD)
    ring_folded = ring_tip < (ring_dip + DETECTION_THRESHOLD)

    # Detect if pinky and thumb are up
    pinky_up = pinky_tip > (pinky_dip + DETECTION_THRESHOLD)
    thumb_up = thumb_tip_x > thumb_mcp_x if is_right_hand else thumb_tip_x < thumb_mcp_x

    # Check if it's a valid Shaka sign (🤙)
    is_shaka = index_folded and middle_folded and ring_folded and pinky_up and thumb_up

    # Update the CHOP value
    if shaka_chop:
        shaka_chop.par.value0 = 1 if is_shaka else 0
