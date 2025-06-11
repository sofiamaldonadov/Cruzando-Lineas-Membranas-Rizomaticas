def onValueChange(channel, sampleIndex, val, prev):
    pose_chop = op('null1')  # Ensure this is your pose data CHOP
    constant_chop = op('bow_detected')


    # Extract Y and Z positions
    nose_y = pose_chop['nose:y'][0]
    nose_z = pose_chop['nose:z'][0]
    left_shoulder_y = pose_chop['left_shoulder:y'][0]
    right_shoulder_y = pose_chop['right_shoulder:y'][0]
    left_hip_y = pose_chop['left_hip:y'][0]
    right_hip_y = pose_chop['right_hip:y'][0]
    left_hip_z = pose_chop['left_hip:z'][0]
    right_hip_z = pose_chop['right_hip:z'][0]
    left_wrist_y = pose_chop['left_wrist:y'][0]
    right_wrist_y = pose_chop['right_wrist:y'][0]

    # Compute averages
    shoulder_y = (left_shoulder_y + right_shoulder_y) / 2
    hip_y = (left_hip_y + right_hip_y) / 2
    hip_z = (left_hip_z + right_hip_z) / 2

    # ** Adjusted Bowing Conditions for 30° Bow **
    head_lowered = nose_y < shoulder_y - 0.01  # Slight head dip
    body_tilted_forward = nose_z < -0.1  # 30° forward tilt instead of deeper bow
    hips_stable = abs(hip_z) < 0.05  # Hips should not move forward

    # ** Hands Visibility Check **
    hands_visible = (left_wrist_y > hip_y) and (right_wrist_y > hip_y)  # Hands should be above hips

    # ** Final Detection (Higher Bow at 30°) **
    bow_detected = head_lowered and body_tilted_forward and hips_stable and hands_visible

    # Output result
    constant_chop.par.value0 = 1 if bow_detected else 0
