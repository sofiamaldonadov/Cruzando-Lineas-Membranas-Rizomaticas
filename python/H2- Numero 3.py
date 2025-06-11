DETECTION_THRESHOLD = 0.02  # Minimum height difference to detect fingers up

def onValueChange(channel, sampleIndex, val, prev):
    num3_chop = op('constant3')  # Constant CHOP for output
    hand_chop = op('h2_number_3')  # CHOP with finger data for second hand


    # Get Y values of finger tips and DIP joints for hand 2
    index_tip = float(hand_chop['h2:index_finger_tip:y'][0])
    index_dip = float(hand_chop['h2:index_finger_dip:y'][0])

    middle_tip = float(hand_chop['h2:middle_finger_tip:y'][0])
    middle_dip = float(hand_chop['h2:middle_finger_dip:y'][0])

    ring_tip = float(hand_chop['h2:ring_finger_tip:y'][0])
    ring_dip = float(hand_chop['h2:ring_finger_dip:y'][0])

    pinky_tip = float(hand_chop['h2:pinky_tip:y'][0])
    pinky_dip = float(hand_chop['h2:pinky_dip:y'][0])

    thumb_tip = float(hand_chop['h2:thumb_tip:y'][0])  

    # Detect fingers up/down
    index_up = index_tip > (index_dip + DETECTION_THRESHOLD)
    middle_up = middle_tip > (middle_dip + DETECTION_THRESHOLD)
    ring_up = ring_tip > (ring_dip + DETECTION_THRESHOLD)

    pinky_down = pinky_tip < pinky_dip
    thumb_down = thumb_tip < 0.3  

    # 3 fingers detected if index, middle, ring are up, and pinky + thumb are down
    is_three_fingers = index_up and middle_up and ring_up and pinky_down and thumb_down


    # Update the constant CHOP
    num3_chop.par.value0 = 1 if is_three_fingers else 0

    return
