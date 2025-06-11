def onValueChange(channel, sampleIndex, val, prev):
    pose_chop = op('buddhists_blessings')  # Ensure this points to your Select CHOP
    constant_chop = op('buddhists_blessings_detected')  # Adjust based on your setup

    # List of required channels
    required_channels = ['left_wrist:y', 'right_wrist:y', 'left_shoulder:y', 
                         'right_shoulder:y', 'left_hip:y', 'right_hip:y']

    # Extract Y positions safely
    left_wrist_y = pose_chop['left_wrist:y'][0]
    right_wrist_y = pose_chop['right_wrist:y'][0]
    left_shoulder_y = pose_chop['left_shoulder:y'][0]
    right_shoulder_y = pose_chop['right_shoulder:y'][0]
    left_hip_y = pose_chop['left_hip:y'][0]
    right_hip_y = pose_chop['right_hip:y'][0]

    # Condition for one hand up near the shoulder
    left_hand_up = left_wrist_y > left_shoulder_y - 0.05  
    right_hand_up = right_wrist_y > right_shoulder_y - 0.05

    # Condition for the opposite hand down near the hip
    left_hand_down = left_wrist_y < left_hip_y + 0.05
    right_hand_down = right_wrist_y < right_hip_y + 0.05

    # Check if either (left up, right down) OR (right up, left down) is true
    buddhist_pose_detected = (left_hand_up and right_hand_down) or (right_hand_up and left_hand_down)

    # Set the CHOP value to 1 if detected, else 0
    constant_chop.par.value0 = 1 if buddhist_pose_detected else 0
