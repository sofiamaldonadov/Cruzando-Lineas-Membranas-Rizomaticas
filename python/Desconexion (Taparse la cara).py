def onValueChange(channel, sampleIndex, val, prev):
    """
    Detects when both hands are touching the shoulders.
    Updates a Constant CHOP to indicate when the user has crossed arms.
    """

    # Get CHOP references
    pose_chop = op('protecting_body')  # Replace with actual Select CHOP name
    constant_chop = op('protecting_body_detected')  # Replace with actual Constant CHOP name


    # Extract available channels
    available_channels = [c.name for c in pose_chop.chans()]

    # Function to safely extract values
    def get_value(channel_name):
        return pose_chop[channel_name][0] if channel_name in available_channels else None

    # Extract wrist positions
    left_wrist_x, left_wrist_y = get_value('left_wrist:x'), get_value('left_wrist:y')
    right_wrist_x, right_wrist_y = get_value('right_wrist:x'), get_value('right_wrist:y')

    # Extract shoulder positions
    left_shoulder_x, left_shoulder_y = get_value('left_shoulder:x'), get_value('left_shoulder:y')
    right_shoulder_x, right_shoulder_y = get_value('right_shoulder:x'), get_value('right_shoulder:y')


    # ✅ **Slightly relaxed thresholds for "touching" detection**
    shoulder_x_threshold = 0.05  # Was 0.02, slightly more forgiving
    shoulder_y_threshold = 0.05  # Was 0.02, allows for slight misalignment

    # **Check if left wrist is touching the right shoulder**
    left_hand_on_right_shoulder = (
        abs(left_wrist_x - right_shoulder_x) < shoulder_x_threshold and
        abs(left_wrist_y - right_shoulder_y) < shoulder_y_threshold
    )

    # **Check if right wrist is touching the left shoulder**
    right_hand_on_left_shoulder = (
        abs(right_wrist_x - left_shoulder_x) < shoulder_x_threshold and
        abs(right_wrist_y - left_shoulder_y) < shoulder_y_threshold
    )

    # ✅ **Ensure both hands are properly detected on shoulders**
    arms_crossed = left_hand_on_right_shoulder and right_hand_on_left_shoulder

    # Update CHOP output
    constant_chop.par.value0 = 1 if arms_crossed else 0


    return
