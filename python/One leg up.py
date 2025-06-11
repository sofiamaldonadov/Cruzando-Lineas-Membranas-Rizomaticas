def onValueChange(channel, sampleIndex, val, prev):
    pose_chop = op('kneeling')  # Ensure this matches your Select CHOP name
    constant_chop = op('kneeling_detected')  # The Constant CHOP for binary output

    # Extract Y positions
    left_knee_y = pose_chop['left_knee:y'][0]
    right_knee_y = pose_chop['right_knee:y'][0]
    left_hip_y = pose_chop['left_hip:y'][0]
    right_hip_y = pose_chop['right_hip:y'][0]
    left_shoulder_y = pose_chop['left_shoulder:y'][0]
    right_shoulder_y = pose_chop['right_shoulder:y'][0]


    # Kneeling Pose Conditions (Adjusted thresholds for better detection)
    left_knee_down = left_knee_y < left_hip_y - 0.2  # Ensure knee is significantly lower than hip
    right_knee_down = right_knee_y < right_hip_y - 0.2
    hips_lowered = (left_hip_y + right_hip_y) / 2 < 0.05  # Ensure hips are low enough
    torso_upright = left_shoulder_y > left_hip_y and right_shoulder_y > right_hip_y  # Ensures upright posture

    return
