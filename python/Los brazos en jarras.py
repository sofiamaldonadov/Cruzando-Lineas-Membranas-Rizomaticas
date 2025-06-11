def onValueChange(channel, sampleIndex, val, prev):
    """
    Detect if ONLY ONE hand (left OR right) is on the hip.
    Removes shoulder height restriction.
    """

    # **Get CHOP references**
    pose_chop = op('one_hand_on_hip')  # The CHOP with pose tracking data
    constant_chop = op('one_hand_on_hip_detected')  # Output CHOP to indicate detection

    # **Extract wrist and hip positions**
    left_wrist_x = pose_chop['left_wrist:x'][0]
    left_wrist_y = pose_chop['left_wrist:y'][0]
    left_wrist_z = pose_chop['left_wrist:z'][0]

    right_wrist_x = pose_chop['right_wrist:x'][0]
    right_wrist_y = pose_chop['right_wrist:y'][0]
    right_wrist_z = pose_chop['right_wrist:z'][0]

    left_hip_x = pose_chop['left_hip:x'][0]
    left_hip_y = pose_chop['left_hip:y'][0]
    left_hip_z = pose_chop['left_hip:z'][0]

    right_hip_x = pose_chop['right_hip:x'][0]
    right_hip_y = pose_chop['right_hip:y'][0]
    right_hip_z = pose_chop['right_hip:z'][0]

    # **Adaptive Threshold Calculation Based on Depth**
    depth_factor = abs((left_hip_z + right_hip_z) / 2)

    def adaptive_threshold(base, depth_factor, min_thresh, max_thresh):
        adaptive = base * (1 + (1.5 / (1 + depth_factor * 5)))
        return min(max(adaptive, min_thresh), max_thresh)

    wrist_x_threshold = adaptive_threshold(0.06, depth_factor, 0.04, 0.10)
    wrist_y_threshold = adaptive_threshold(0.06, depth_factor, 0.03, 0.10)
    wrist_z_threshold = adaptive_threshold(0.10, depth_factor, 0.04, 0.12)

    # **Check if the left hand is on the hip**
    left_on_hip = (
        abs(left_wrist_x - left_hip_x) < wrist_x_threshold and
        abs(left_wrist_y - left_hip_y) < wrist_y_threshold and
        abs(left_wrist_z - left_hip_z) < wrist_z_threshold
    )

    # **Check if the right hand is on the hip**
    right_on_hip = (
        abs(right_wrist_x - right_hip_x) < wrist_x_threshold and
        abs(right_wrist_y - right_hip_y) < wrist_y_threshold and
        abs(right_wrist_z - right_hip_z) < wrist_z_threshold
    )

    # **Only ONE hand must be on the hip (XOR condition)**
    one_hand_on_hip_detected = (left_on_hip and not right_on_hip) or (right_on_hip and not left_on_hip)


    # **Update the Constant CHOP**
    constant_chop.par.value0 = 1 if one_hand_on_hip_detected else 0
