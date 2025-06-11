def onValueChange(channel, sampleIndex, val, prev):
    pose_chop = op('select1')  # Ensure this is the correct Select CHOP name
    constant_chop = op('leg_up_detected')  # This should match your Constant CHOP name

    # Extract Y positions
    left_knee_y = pose_chop['left_knee:y'][0]
    right_knee_y = pose_chop['right_knee:y'][0]
    left_hip_y = pose_chop['left_hip:y'][0]
    right_hip_y = pose_chop['right_hip:y'][0]
    left_shoulder_y = pose_chop['left_shoulder:y'][0]
    right_shoulder_y = pose_chop['right_shoulder:y'][0]


    # One Leg Up Pose Conditions (Lowered threshold to +0.02)
    left_leg_raised = left_knee_y > left_hip_y + 0.02  # Looser detection
    right_leg_raised = right_knee_y > right_hip_y + 0.02
    torso_upright = left_shoulder_y > left_hip_y and right_shoulder_y > right_hip_y  # Ensures the person is standing


    return
