def onValueChange(channel, sampleIndex, val, prev):
    """
    Detects when ONE fist (right OR left) is raised above or next to the shoulder.
    Ensures the fist is fully closed before activation, even at different angles.
    """

    # **Get CHOP references**
    pose_chop = op('raised_fist')  # CHOP containing body tracking data
    constant_chop = op('raised_fist_detected')  # CHOP to output detection result

    # **Extract required values using the correct channel names**
    try:
        lw_y = pose_chop['null1:left_wrist:y'][0]
        rw_y = pose_chop['null1:right_wrist:y'][0]
        le_y = pose_chop['null1:left_elbow:y'][0]
        re_y = pose_chop['null1:right_elbow:y'][0]
        ls_y = pose_chop['null1:left_shoulder:y'][0]
        rs_y = pose_chop['null1:right_shoulder:y'][0]

        li_y = pose_chop['null1:left_index:y'][0]
        ri_y = pose_chop['null1:right_index:y'][0]
        lp_y = pose_chop['null1:left_pinky:y'][0]
        rp_y = pose_chop['null1:right_pinky:y'][0]
        lt_y = pose_chop['null1:left_thumb:y'][0]
        rt_y = pose_chop['null1:right_thumb:y'][0]
    except KeyError:
        return  # Skip execution if a required channel is missing

    # **1️⃣ Wrist must be above or next to the shoulder**
    SHOULDER_MARGIN = 0.08  # Increased margin to allow more flexibility
    left_hand_raised = lw_y > (ls_y - SHOULDER_MARGIN) and lw_y > le_y
    right_hand_raised = rw_y > (rs_y - SHOULDER_MARGIN) and rw_y > re_y

    # **2️⃣ Fingers must be fully curled into a fist**
    FIST_THRESHOLD = 0.05  # Increased to allow slight variation in fist shape
    THUMB_TOLERANCE = 0.07  # Allows thumbs to sit slightly higher

    left_fist_closed = (
        (li_y - lw_y) < FIST_THRESHOLD and
        (lp_y - lw_y) < FIST_THRESHOLD and
        (lt_y - lw_y) < THUMB_TOLERANCE
    )

    right_fist_closed = (
        (ri_y - rw_y) < FIST_THRESHOLD and
        (rp_y - rw_y) < FIST_THRESHOLD and
        (rt_y - rw_y) < THUMB_TOLERANCE
    )

    # **3️⃣ Final Detection: ONE raised fist**
    left_fist_detected = left_hand_raised and left_fist_closed
    right_fist_detected = right_hand_raised and right_fist_closed

    one_fist_raised = (left_fist_detected and not right_fist_detected) or \
                      (right_fist_detected and not left_fist_detected)

    # **Update the Constant CHOP Output**
    constant_chop.par.value0 = 1 if one_fist_raised else 0
