def onValueChange(channel, sampleIndex, val, prev):
    """
    Detects when both hands cover the eyes or nose (if eyes are missing).
    Updates a Constant CHOP to indicate when the face is hidden.
    """

    # Get CHOP references
    pose_chop = op('disconnection')  # Replace with actual Select CHOP name
    constant_chop = op('disconnection_detected')  # Replace with actual Constant CHOP name

    # Ensure CHOPs exist
    if not pose_chop or not constant_chop:
        return  # Exit if CHOPs are missing

    # Ensure CHOP has data
    if pose_chop.numChans == 0:
        return  # Exit if 'disconnection' CHOP has no data

    # Extract available channels
    available_channels = [c.name for c in pose_chop.chans()]

    # Check if eye tracking is available
    eye_tracking_available = all(chan in available_channels for chan in ['left_eye:x', 'left_eye:y', 'right_eye:x', 'right_eye:y'])

    # Choose reference points (eyes if available, otherwise nose)
    if eye_tracking_available:
        ref_x_left, ref_y_left = pose_chop['left_eye:x'][0], pose_chop['left_eye:y'][0]
        ref_x_right, ref_y_right = pose_chop['right_eye:x'][0], pose_chop['right_eye:y'][0]
    else:
        ref_x_left, ref_y_left = pose_chop['nose:x'][0], pose_chop['nose:y'][0]
        ref_x_right, ref_y_right = ref_x_left, ref_y_left  # Use same nose values for both sides

    # Get wrist positions
    left_wrist_x, left_wrist_y = pose_chop['left_wrist:x'][0], pose_chop['left_wrist:y'][0]
    right_wrist_x, right_wrist_y = pose_chop['right_wrist:x'][0], pose_chop['right_wrist:y'][0]

    # ✅ **Make X-axis threshold stricter**
    wrist_x_threshold = 0.08  # Previous: 0.12 (Stricter, hands must be closer)
    wrist_y_threshold = 0.10  # Hands should be at eye level or slightly above

    # **Check if hands are covering the reference points**
    left_hand_on_face = (
        abs(left_wrist_x - ref_x_left) < wrist_x_threshold and
        abs(left_wrist_y - ref_y_left) < wrist_y_threshold
    )

    right_hand_on_face = (
        abs(right_wrist_x - ref_x_right) < wrist_x_threshold and
        abs(right_wrist_y - ref_y_right) < wrist_y_threshold
    )

    # **Both hands covering the face detection**
    face_hidden = left_hand_on_face and right_hand_on_face

    # **Update CHOP output**
    constant_chop.par.value0 = 1 if face_hidden else 0  

    return
