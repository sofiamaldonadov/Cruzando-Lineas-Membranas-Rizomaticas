def onValueChange(channel, sampleIndex, val, prev):
    """
    Improved 'surrender' pose detection with finger openness check using 'y tip' values.
    """

    # **Get CHOP references**
    pose_chop = op('surrender')  # CHOP with pose tracking data
    constant_chop = op('surrender_detected')  # Output CHOP to indicate detection

    # **Extract necessary body tracking values**
    lw_y = pose_chop['left_wrist:y'][0]
    rw_y = pose_chop['right_wrist:y'][0]
    ls_y = pose_chop['left_shoulder:y'][0]
    rs_y = pose_chop['right_shoulder:y'][0]
    le_y = pose_chop['left_elbow:y'][0]
    re_y = pose_chop['right_elbow:y'][0]

    # **Finger Tip Y Values**
    li_y = pose_chop['left_index:y'][0]
    ri_y = pose_chop['right_index:y'][0]
    lp_y = pose_chop['left_pinky:y'][0]
    rp_y = pose_chop['right_pinky:y'][0]
    lt_y = pose_chop['left_thumb:y'][0]
    rt_y = pose_chop['right_thumb:y'][0]

    lw_x = pose_chop['left_wrist:x'][0]
    rw_x = pose_chop['right_wrist:x'][0]

    # **1️⃣ Hands Raised Above Shoulders and Elbows (with small tolerance)**
    arms_raised = ((lw_y > ls_y - 0.03 and rw_y > rs_y - 0.03) and
                   (lw_y > le_y and rw_y > re_y))

    # **2️⃣ Palms Facing Forward (same logic as before)**
    palms_forward = ((li_y > lw_y) and (ri_y > rw_y))

    # **3️⃣ Hands Apart (Ensuring it's a surrender pose and not a clap)**
    hands_apart = abs(lw_x - rw_x) > 0.2  # Adjust if needed

    # **4️⃣ Fingers Open (Ensuring hands are not closed fists)**
    fingers_open = ((li_y > lw_y + 0.04) and  
                    (lp_y > lw_y + 0.04) and  
                    (lt_y > lw_y + 0.04) and  
                    (ri_y > rw_y + 0.04) and  
                    (rp_y > rw_y + 0.04) and  
                    (rt_y > rw_y + 0.04))

    # **Final Pose Detection**
    surrender_detected = arms_raised and palms_forward and hands_apart and fingers_open

    # **Update the Constant CHOP Output**
    constant_chop.par.value0 = 1 if surrender_detected else 0
