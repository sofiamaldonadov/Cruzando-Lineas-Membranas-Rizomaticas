# Detection thresholds
DETECTION_THRESHOLD = 0.02  # Minimum height difference for "up" detection
TOUCH_THRESHOLD = 0.05  # Maximum distance between thumb and index tip to detect touch

def onValueChange(channel, sampleIndex, val, prev):
    # Get CHOP references
    ok_chop_h2 = op('ok_sign_h2_detected')  # Output CHOP for second-hand detection
    hand_chop_h2 = op('ok_sign_h2')  # CHOP containing second-hand tracking data

    # Ensure `hand_chop_h2` exists and contains data
    if not hand_chop_h2 or not hand_chop_h2.numChans:
        return

    try:
        # Get Y values for detecting finger positions
        index_tip_y = float(hand_chop_h2['h2:index_finger_tip:y'][0])
        thumb_tip_y = float(hand_chop_h2['h2:thumb_tip:y'][0])

        middle_tip_y = float(hand_chop_h2['h2:middle_finger_tip:y'][0])
        middle_dip_y = float(hand_chop_h2['h2:middle_finger_dip:y'][0])
        ring_tip_y = float(hand_chop_h2['h2:ring_finger_tip:y'][0])
        ring_dip_y = float(hand_chop_h2['h2:ring_finger_dip:y'][0])
        pinky_tip_y = float(hand_chop_h2['h2:pinky_tip:y'][0])
        pinky_dip_y = float(hand_chop_h2['h2:pinky_dip:y'][0])

    except KeyError:
        return

    # Calculate the distance between thumb and index finger tip
    thumb_index_distance = abs(thumb_tip_y - index_tip_y)
    thumb_index_touching = thumb_index_distance < TOUCH_THRESHOLD  # True if close

    # Detect if the three fingers are up
    middle_up = middle_tip_y > (middle_dip_y + DETECTION_THRESHOLD)
    ring_up = ring_tip_y > (ring_dip_y + DETECTION_THRESHOLD)
    pinky_up = pinky_tip_y > (pinky_dip_y + DETECTION_THRESHOLD)

    # OK sign detected if thumb & index touch and other fingers are up
    is_ok_sign_h2 = thumb_index_touching and middle_up and ring_up and pinky_up

    # Update the CHOP output
    if ok_chop_h2:
        ok_chop_h2.par.value0 = 1 if is_ok_sign_h2 else 0
