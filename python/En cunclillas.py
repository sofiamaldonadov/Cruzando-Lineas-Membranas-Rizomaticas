def onValueChange(channel, sampleIndex, val, prev):
    """
    Detects when the user is squatting based on:
    1. Hips being close to the ankles
    2. Shoulders lowering more than normal
    Updates a Constant CHOP to indicate when the user is squatting.
    """

    # 🔹 Get CHOP references
    pose_chop = op('squatting')  # Replace with your Select CHOP name
    constant_chop = op('squatting_detected')  # Replace with your Constant CHOP name

    # Extract available channels
    available_channels = [c.name for c in pose_chop.chans()]

    # Function to safely extract values
    def get_value(channel_name):
        return pose_chop[channel_name][0] if channel_name in available_channels else 0

    # Extract key positions
    left_hip_y, right_hip_y = get_value('left_hip:y'), get_value('right_hip:y')
    left_knee_y, right_knee_y = get_value('left_knee:y'), get_value('right_knee:y')
    left_ankle_y, right_ankle_y = get_value('left_ankle:y'), get_value('right_ankle:y')
    left_shoulder_y, right_shoulder_y = get_value('left_shoulder:y'), get_value('right_shoulder:y')

    # Calculate the average positions
    avg_hip_y = (left_hip_y + right_hip_y) / 2
    avg_knee_y = (left_knee_y + right_knee_y) / 2
    avg_ankle_y = (left_ankle_y + right_ankle_y) / 2
    avg_shoulder_y = (left_shoulder_y + right_shoulder_y) / 2

    # 🔹 Set Thresholds (Adjust if needed)
    hip_near_ankle_threshold = 0.20  # Adjust this value to fine-tune sensitivity
    shoulder_lower_threshold = 0.55  # Adjust this value to make it less strict

    # **Condition 1: Hips close to ankles**
    hips_near_ankles = abs(avg_hip_y - avg_ankle_y) < hip_near_ankle_threshold

    # **Condition 2: Shoulders lowered more than normal**
    shoulders_lowered = avg_shoulder_y < shoulder_lower_threshold

    # **Final Check: Squatting condition**
    squatting = hips_near_ankles and shoulders_lowered

    # 🔹 Update CHOP output
    constant_chop.par.value0 = 1 if squatting else 0

    return
