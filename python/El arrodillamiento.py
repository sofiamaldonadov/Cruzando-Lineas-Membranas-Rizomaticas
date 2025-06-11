def onValueChange(channel, sampleIndex, val, prev):
    pose_chop = op('hands_on_hips')  # Confirm your CHOP name
    constant_chop = op('hands_on_hips_detected')  # Output CHOP for results

    # Extract wrist and hip positions
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

    # Calculate depth factor (average hip depth)
    depth_factor = abs((left_hip_z + right_hip_z) / 2)

    # Adaptive thresholds with enforced minimum and maximum thresholds
    def adaptive_threshold(base, depth_factor, min_thresh, max_thresh):
        adaptive = base * (1 + (1.5 / (1 + depth_factor * 5)))
        return min(max(adaptive, min_thresh), max_thresh)

    # Define min and max thresholds to maintain accuracy at different distances
    wrist_x_threshold = adaptive_threshold(0.08, depth_factor, 0.06, 0.15)
    wrist_y_threshold = adaptive_threshold(0.08, depth_factor, 0.05, 0.12)
    wrist_z_threshold = adaptive_threshold(0.15, depth_factor, 0.05, 0.18)

    # **Check if left hand is on hip**
    left_on_hip = (
        abs(left_wrist_x - left_hip_x) < wrist_x_threshold and
        abs(left_wrist_y - left_hip_y) < wrist_y_threshold and
        abs(left_wrist_z - left_hip_z) < wrist_z_threshold
    )

    # **Check if right hand is on hip**
    right_on_hip = (
        abs(right_wrist_x - right_hip_x) < wrist_x_threshold and
        abs(right_wrist_y - right_hip_y) < wrist_y_threshold and
        abs(right_wrist_z - right_hip_z) < wrist_z_threshold
    )

    # **Both hands on hips detection (STRICT MODE)**
    hands_on_hips_detected = left_on_hip and right_on_hip


    # **Update Constant CHOP to indicate detection**
    constant_chop.par.value0 = 1 if hands_on_hips_detected else 0
