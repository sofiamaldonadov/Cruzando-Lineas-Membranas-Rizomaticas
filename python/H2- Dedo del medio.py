DETECTION_THRESHOLD = 0.010  # Adjust as needed

def onValueChange(channel, sampleIndex, val, prev):
    pinky_chop = op('pinky_finger')  # CHOP with finger data
    detected_chop = op('pinky_finger_detected')  # Output CHOP

    try:
        # Y values for fingers
        pinky_tip = float(pinky_chop['h1:pinky_tip:y'][0])
        pinky_dip = float(pinky_chop['h1:pinky_dip:y'][0])
        ring_tip = float(pinky_chop['h1:ring_finger_tip:y'][0])
        ring_dip = float(pinky_chop['h1:ring_finger_dip:y'][0])
        middle_tip = float(pinky_chop['h1:middle_finger_tip:y'][0])
        middle_dip = float(pinky_chop['h1:middle_finger_dip:y'][0])
        index_tip = float(pinky_chop['h1:index_finger_tip:y'][0])
        index_dip = float(pinky_chop['h1:index_finger_dip:y'][0])

        # X values for thumb
        thumb_tip_x = float(pinky_chop['h1:thumb_tip:x'][0])
        thumb_ip_x = float(pinky_chop['h1:thumb_ip:x'][0])
    except KeyError:
        return  # Skip if any channel is missing

    # Gesture logic
    pinky_up = pinky_tip > (pinky_dip + DETECTION_THRESHOLD)
    ring_folded = ring_tip < (ring_dip - DETECTION_THRESHOLD)
    middle_folded = middle_tip < (middle_dip - DETECTION_THRESHOLD)
    index_folded = index_tip < (index_dip - DETECTION_THRESHOLD)
    thumb_folded = thumb_tip_x < (thumb_ip_x - DETECTION_THRESHOLD)

    pinky_gesture = pinky_up and ring_folded and middle_folded and index_folded and thumb_folded

    # Update the constant CHOP
    detected_chop.par.value0 = 1 if pinky_gesture else 0

    return
