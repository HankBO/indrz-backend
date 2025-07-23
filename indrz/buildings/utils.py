import pandas as pd
import numpy as np


def room_estimation(fp_input_df: pd.DataFrame, fp_datase: pd.DataFrame):
    ALPHA = 0.5  # Adjust this value based on experimentation
    """
    Estimate the room based on input fingerprint: [{"bssid": string, "rssi": integer}].
    fp_datase: bssid, fp_id, room_external_id, site_id, rssi, floor_num
    """
    fp_ids = fp_datase['fp_id'].unique()
    distances = []
    simiarities = []

    for fp_id in fp_ids:
        fp = fp_datase[fp_datase['fp_id'] == fp_id]
        if len(fp) == 0:
            continue

        # Calculate the euclidean distance between the input fingerprint and the database fingerprint
        # if bssid in fp_id not detected in fp_input_df, set rssi = -120
        # convert fingerprint to np.array
        fp_db_rssi_array = np.array([item['rssi'] for item in fp.to_dict('records')])
        # convert fp_input to np.array, if bssid not in fp_input_df, set rssi = -120, with the same order by fp_db's bssid
        fp_input_rssi_array = np.array([
            fp_input_df.loc[fp_input_df['bssid'] == item['bssid'], 'rssi'].values[0]
            if item['bssid'] in fp_input_df['bssid'].values else -120 for item in fp.to_dict('records')
        ])
        # print(fp_db_rssi_array, fp_input_rssi_array)
        assert len(fp_db_rssi_array) == len(fp_input_rssi_array), "Input fingerprint and database fingerprint must have the same length"
        distance = np.linalg.norm(fp_input_rssi_array - fp_db_rssi_array)
        distances.append(distance)

        # Calculate the similarity between the input fingerprint and the database fingerprint
        N_aps_deteced_both = np.sum((fp_input_rssi_array != -120) & (fp_db_rssi_array != -120))
        N_aps_in_fp_input = len(fp_input_df)
        similarity = 1 / (distance * ( 1 - ALPHA * (N_aps_deteced_both / N_aps_in_fp_input)))
        simiarities.append(similarity)

    # Find the fingerprint with the minimum distance
    if len(distances) == 0:
        return None

    min_distance_index = np.argmin(distances)
    best_fp_id = fp_ids[min_distance_index]
    best_similarity = simiarities[min_distance_index]

    print("Estimations: ",distances, fp_datase[fp_datase['fp_id'] == best_fp_id].iloc[0]['room_external_id'], best_similarity)
    return fp_datase[fp_datase['fp_id'] == best_fp_id].iloc[0]['room_external_id'], best_similarity
