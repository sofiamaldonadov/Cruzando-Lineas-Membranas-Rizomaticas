def onValueChange(channel, sampleIndex, val, prev):
    pose_chop = op('airport_stance')  # Ensure this is your Select CHOP name
    constant_chop = op('airport_stance_detected')  # The Constant CHOP for binary output

    # Extract Y positions
    left_wrist_y = pose_chop['left_wrist:y'][0]
    right_wrist_y = pose_chop['right_wrist:y'][0]
    left_elbow_y = pose_chop['left_elbow:y'][0]
    right_elbow_y = pose_chop['right_elbow:y'][0]
    left_shoulder_y = pose_chop['left_shoulder:y'][0]
    right_shoulder_y = pose_chop['right_shoulder:y'][0]
    left_hip_y = pose_chop['left_hip:y'][0]
    right_hip_y = pose_chop['right_hip:y'][0]


    # Airport Stance Conditions
    hands_above_shoulders = left_wrist_y > left_shoulder_y and right_wrist_y > right_shoulder_y
    elbows_near_shoulders = abs(left_elbow_y - left_shoulder_y) < 0.1 and abs(right_elbow_y - right_shoulder_y) < 0.1
    torso_upright = left_shoulder_y > left_hip_y and right_shoulder_y > right_hip_y  # Ensures person is standing

    return
