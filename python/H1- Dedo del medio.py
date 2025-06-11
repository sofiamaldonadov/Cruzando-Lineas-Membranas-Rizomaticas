DETECTION_THRESHOLD = 0.02  # Adjust as needed

def onValueChange(channel, sampleIndex, val, prev):
    middle_chop = op('h2_middle_finger')  # Ensure this CHOP has the correct second-hand data
    detected_chop = op('h2_middle_finger_detected')  # Output CHOP

    # Get Y positions for middle, index, and ring fingers (Second Hand)
    middle_tip = float(middle_chop['h2:middle_finger_tip:y'][0])
    middle_dip = float(middle_chop['h2:middle_finger_dip:y'][0])
    index_tip = float(middle_chop['h2:index_finger_tip:y'][0])
    index_dip = float(middle_chop['h2:index_finger_dip:y'][0])
    ring_tip = float(middle_chop['h2:ring_finger_tip:y'][0])
    ring_dip = float(middle_chop['h2:ring_finger_dip:y'][0])

    # Conditions:
    middle_up = middle_tip > (middle_dip + DETECTION_THRESHOLD)  # Middle finger raised
    index_folded = index_tip < (index_dip - DETECTION_THRESHOLD)  # Index finger bent
    ring_folded = ring_tip < (ring_dip - DETECTION_THRESHOLD)  # Ring finger bent

    # Final check: Middle finger up & others folded
    middle_gesture = middle_up and index_folded and ring_folded

    # Debugging output
    print(f"(H2) Middle Gesture | Middle: {middle_up}, Index Folded: {index_folded}, Ring Folded: {ring_folded} | Detected? {'YES' if middle_gesture else 'NO'}")

    # Update the constant CHOP
    detected_chop.par.value0 = 1 if middle_gesture else 0

    return
