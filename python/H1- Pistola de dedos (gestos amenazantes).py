DETECTION_THRESHOLD = 0.01
MAX_THUMB_DISTANCE = 0.1  # Upper limit to avoid weird positions

def onValueChange(channel, sampleIndex, val, prev):
    pinky_chop = op('h2_pinky_finger')
    detected_chop = op('h2_pinky_finger_detected')

    try:
        pinky_tip = float(pinky_chop['h2:pinky_tip:y'][0])
        pinky_dip = float(pinky_chop['h2:pinky_dip:y'][0])
        ring_tip = float(pinky_chop['h2:ring_finger_tip:y'][0])
        ring_dip = float(pinky_chop['h2:ring_finger_dip:y'][0])
        middle_tip = float(pinky_chop['h2:middle_finger_tip:y'][0])
        middle_dip = float(pinky_chop['h2:middle_finger_dip:y'][0])
        index_tip = float(pinky_chop['h2:index_finger_tip:y'][0])
        index_dip = float(pinky_chop['h2:index_finger_dip:y'][0])
        thumb_tip_x = float(pinky_chop['h2:thumb_tip:x'][0])
        thumb_ip_x = float(pinky_chop['h2:thumb_ip:x'][0])
    except KeyError:
        return

    pinky_up = pinky_tip > (pinky_dip + DETECTION_THRESHOLD)
    ring_folded = ring_tip < (ring_dip - DETECTION_THRESHOLD)
    middle_folded = middle_tip < (middle_dip - DETECTION_THRESHOLD)
    index_folded = index_tip < (index_dip - DETECTION_THRESHOLD)

    # ✅ Direction-agnostic thumb check
    thumb_distance = abs(thumb_tip_x - thumb_ip_x)
    thumb_folded = DETECTION_THRESHOLD < thumb_distance < MAX_THUMB_DISTANCE

    pinky_gesture = pinky_up and ring_folded and middle_folded and index_folded and thumb_folded

    detected_chop.par.value0 = 1 if pinky_gesture else 0

    return
