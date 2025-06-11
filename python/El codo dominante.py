def onValueChange(channel, sampleIndex, val, prev):
    pose_chop = op('null1')  # Using 'null1' to get pose data
    constant_chop = op('arms_crossed_detected')  # Output CHOP

    # Check if required channels exist
    required_channels = ['left_wrist:x', 'right_wrist:x', 'left_elbow:x', 'right_elbow:x',
                         'left_shoulder:x', 'right_shoulder:x', 'left_wrist:y', 'right_wrist:y',
                         'left_elbow:y', 'right_elbow:y', 'left_hip:y', 'right_hip:y']
    existing_channels = [ch.name for ch in pose_chop.chans()]
    

    # Extract positions
    left_wrist_x = pose_chop['left_wrist:x'][0]
    right_wrist_x = pose_chop['right_wrist:x'][0]
    left_elbow_x = pose_chop['left_elbow:x'][0]
    right_elbow_x = pose_chop['right_elbow:x'][0]
    left_shoulder_x = pose_chop['left_shoulder:x'][0]
    right_shoulder_x = pose_chop['right_shoulder:x'][0]

    left_wrist_y = pose_chop['left_wrist:y'][0]
    right_wrist_y = pose_chop['right_wrist:y'][0]
    left_elbow_y = pose_chop['left_elbow:y'][0]
    right_elbow_y = pose_chop['right_elbow:y'][0]
    
    left_hip_y = pose_chop['left_hip:y'][0]
    right_hip_y = pose_chop['right_hip:y'][0]

    # Estimate the average hip position (waistline)
    waist_y = (left_hip_y + right_hip_y) / 2

    # **Looser hand height requirement**
    hands_raised = (left_wrist_y > waist_y + 0.05) and (right_wrist_y > waist_y + 0.05)  # Loosened from +0.1 to +0.05

    # **Looser wrist crossing detection**
    left_wrist_crossed = left_wrist_x > right_shoulder_x - 0.05  # Allow slight buffer
    right_wrist_crossed = right_wrist_x < left_shoulder_x + 0.05  # Allow slight buffer

    # **Looser elbow distance requirement**
    elbow_distance = abs(left_elbow_x - right_elbow_x)
    elbows_close = elbow_distance < 0.2  # Loosened from 0.1 to 0.2

    # **Looser wrist height requirement**
    wrist_near_elbows = (left_wrist_y < left_elbow_y + 0.1) and (right_wrist_y < right_elbow_y + 0.1)  # Loosened from +0.05 to +0.1

    # **Final detection: All conditions must be met**
    arms_crossed = hands_raised and left_wrist_crossed and right_wrist_crossed and elbows_close and wrist_near_elbows

    # Output result
    constant_chop.par.value0 = 1 if arms_crossed else 0
