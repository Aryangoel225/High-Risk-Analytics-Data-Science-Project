import streamlit as st
import datetime
import pandas as pd


st.title("Ranking")
#load data
df_pre = pd.read_csv("Newnew_dataset.csv")
df_pre["COUNT"] = 1 #lazy, but keeps track of number of rows when we group categories

# -------------------------------------------- #
# ----------- RANKING AND FILTERS ------------ #
# -------------------------------------------- #

left, right = st.columns(2)
with left:
    # ----------- MAIN RANKING ------------ #
    #Ranks
    st.header("Rank Category")
    rank_options = [
        "Most Frequent Crash Locations",
        "Most Frequent Crash Locations + Weighted",
        "Most Dangerous Crash Locations"
    ]
    ranking_choice = st.selectbox("Rank", rank_options)

with right:
    # ----------- GROUP BY ------------ #
    st.header("Group By")
    group_options = [
        "Street",
        "Location"
    ]
    group_choice = st.selectbox("Group By..", group_options)

# ------------- FILTERS --------------- #
#Filters
st.header("Filters")
st.divider()
date_col, damage_col, crash_col = st.columns(3)
injury_col, cause_col, lighting_col = st.columns(3)
st.divider()

#Date
with date_col:
    date_col.write("**Date:**")
    date_start = date_col.date_input(
        label="Start Date",
        value=pd.to_datetime('2017-10-24'),
        min_value=pd.to_datetime('2017-10-24'),
        max_value=pd.to_datetime('2025-10-24')
    )
    date_end = date_col.date_input(
        label="End Date:",
        value=pd.to_datetime('2025-10-24'),
        min_value=pd.to_datetime('2017-10-24'),
        max_value=pd.to_datetime('2025-10-24')
    )

#Damage
with damage_col:
    damage_col.write("**Damage:**")
    damage_less = damage_col.checkbox(label='$500 OR LESS')
    damage_mid = damage_col.checkbox(label='\$501 - \$1,500')
    damage_high = damage_col.checkbox(label='OVER $1,500')

#Crash Type
with crash_col:
    crash_col.write("**Crash Type:**")
    crash_drive = crash_col.checkbox(label='NO INJURY / DRIVE AWAY')
    crash_injury = crash_col.checkbox(label='INJURY AND / OR TOW DUE TO CRASH')

#Injures
with injury_col:
    injury_col.write("**Injuries:**")
    #['NO INDICATION OF INJURY', 'REPORTED, NOT EVIDENT', 'INCAPACITATING INJURY', 'NONINCAPACITATING INJURY', 'FATAL']
    injury_non = injury_col.checkbox(label='No Injury')
    injury_nonincapacitating = injury_col.checkbox(label='Non-Incapacitating')
    injury_incapacitating = injury_col.checkbox(label='Incapacitating')
    injury_fatal = injury_col.checkbox(label='Fatal')

#Primary/Secondary Cause
with cause_col:
    cause_col.write("**Cause of Crash:**")
    cause_user = cause_col.checkbox(label="User Error")
    cause_nonuser = cause_col.checkbox(label="None-User Error")
    cause_vehicle = cause_col.checkbox(label="Vehicle Error")

    user_error = ['DRIVING SKILLS/KNOWLEDGE/EXPERIENCE',
        'FAILING TO REDUCE SPEED TO AVOID CRASH',
        'IMPROPER OVERTAKING/PASSING', 'FOLLOWING TOO CLOSELY',
        'DISTRACTION - FROM OUTSIDE VEHICLE',
        'FAILING TO YIELD RIGHT-OF-WAY', 'DISREGARDING STOP SIGN',
            'IMPROPER LANE USAGE',
        'IMPROPER TURNING/NO SIGNAL',
        'OPERATING VEHICLE IN ERRATIC, RECKLESS, CARELESS, NEGLIGENT OR AGGRESSIVE MANNER',
        'IMPROPER BACKING', 'DISTRACTION - FROM INSIDE VEHICLE',
        'DRIVING ON WRONG SIDE/WRONG WAY', 'DISREGARDING TRAFFIC SIGNALS',
        'CELL PHONE USE OTHER THAN TEXTING', 'PHYSICAL CONDITION OF DRIVER', 'DISREGARDING OTHER TRAFFIC SIGNS',
        'RELATED TO BUS STOP',  'DISREGARDING ROAD MARKINGS',
        'TURNING RIGHT ON RED',
        'UNDER THE INFLUENCE OF ALCOHOL/DRUGS (USE WHEN ARREST IS EFFECTED)',
        'HAD BEEN DRINKING (USE WHEN ARREST IS NOT MADE)', 'TEXTING',
            'OBSTRUCTED CROSSWALKS',
        'DISTRACTION - OTHER ELECTRONIC DEVICE (NAVIGATION DEVICE, DVD PLAYER, ETC.)',
        'PASSING STOPPED SCHOOL BUS', 'DISREGARDING YIELD SIGN',
        'BICYCLE ADVANCING LEGALLY ON RED LIGHT',
        'MOTORCYCLE ADVANCING LEGALLY ON RED LIGHT',
        'EXCEEDING AUTHORIZED SPEED LIMIT',
        'EXCEEDING SAFE SPEED FOR CONDITIONS']
    non_user_error = [
        'ANIMAL', 'ROAD ENGINEERING/SURFACE/MARKING DEFECTS', 'VISION OBSCURED (SIGNS, TREE LIMBS, BUILDINGS, ETC.)',
        'EVASIVE ACTION DUE TO ANIMAL, OBJECT, NONMOTORIST', 'WEATHER', 'ROAD CONSTRUCTION/MAINTENANCE',
    ]
    vehicle_error = [
        'EQUIPMENT - VEHICLE CONDITION'
    ]

#Lighting
with lighting_col:
    lighting_col.write("**Type of Lighting**")
    lighting_cond = lighting_col.multiselect("Lighting Conditions", ['DARKNESS, LIGHTED ROAD', 'DARKNESS', 'UNKNOWN', 'DAYLIGHT',
        'DAWN', 'DUSK'])

# -------------------------------------------- #
# ----- DATASET CLEANING AND FILTERING  ------ #
# -------------------------------------------- #
if st.button("calculate"):
    df = df_pre.copy()

    # Approximate conversion: 1 degree ≈ 111,000 meters
    # For 50 meters, delta = 50 / 111000 ≈ 0.00045 degrees
    delta = 0.00045

    # Create grid identifiers for 50m squares
    df['LAT_BIN'] = (df['LATITUDE'] / delta).round().astype(int)
    df['LON_BIN'] = (df['LONGITUDE'] / delta).round().astype(int)

    # Combine bins into one label
    df['LOCATION_BIN'] = df['LAT_BIN'].astype(str) + "_" + df['LON_BIN'].astype(str)

    # City wide data only begins post September 2017, so we only track crashes post October 2017,
    # to be safe
    #Specifically, we choose the cutoff date to be October 24, because concidentally that's what
    # our data goes to (25-10-24), so exactly 9 years
    
    #Filter Data

    # ------ Date ------ #
    # ------------------ #
    df["CRASH_DATE_ONLY"] = pd.to_datetime(df["CRASH_DATE_ONLY"])
    date_start = datetime.datetime.combine(date_start, datetime.time.min)
    date_end = datetime.datetime.combine(date_end, datetime.time.max)
    df = df[(df["CRASH_DATE_ONLY"] >= date_start) & (df["CRASH_DATE_ONLY"] <= date_end)]

    # ----- Damage ----- #
    # ------------------ #
    damage_arr = []
    if damage_less:
        damage_arr.append("$500 OR LESS")
    if damage_mid:
        damage_arr.append("$501 - $1,500")
    if damage_high:
        damage_arr.append("OVER $1,500")

    if damage_arr:
        df = df[df["DAMAGE"].isin(damage_arr)]

    # --- Crash Type --- #
    # ------------------ #
    crash_types = []
    if crash_drive:
        crash_types.append("NO INJURY / DRIVE AWAY")
    if crash_injury:
        crash_types.append("INJURY AND / OR TOW DUE TO CRASH")

    if crash_types:  # Only filter if something is selected
        df = df[df["CRASH_TYPE"].isin(crash_types)]
    
    # ---- Injuries ---- #
    # ------------------ #
    injury_conditions = pd.Series([False] * len(df))  # start with all False

    if injury_non:
        injury_conditions |= (df["INJURY_SCORE"] == 0)
    if injury_nonincapacitating:
        injury_conditions |= (df["INJURIES_NON_INCAPACITATING"] > 0)
    if injury_incapacitating:
        injury_conditions |= (df["INJURIES_INCAPACITATING"] > 0)
    if injury_fatal:
        injury_conditions |= (df["INJURIES_FATAL"] > 0)  # replace with your fatal column

    if injury_conditions.any():  # Only filter if any condition is True
        df = df[injury_conditions]

    # ----- Cause ------ #
    # ------------------ #
    cause_arr = []

    if cause_user:
        cause_arr += user_error
    if cause_nonuser:
        cause_arr += non_user_error
    if cause_vehicle:
        cause_arr += vehicle_error

    if cause_arr:
        df = df[df["PRIMARY_CONTRIBUTORY_CAUSE"].isin(cause_arr)]

    # ---- Lighting ---- #
    # ------------------ #
    if lighting_cond:  # Only filter if some lighting conditions selected
        df = df[df["LIGHTING_CONDITION"].isin(lighting_cond)]

    # -------------------------------------------- #
    # ----------- RANKING LOGIC ------------------- #
    # -------------------------------------------- #
    if group_choice == "Street":
        ranking = df.groupby('STREET_NAME').agg("sum", numeric_only=True)
    elif group_choice == "Location":
        ranking = df.groupby('LOCATION_BIN').agg("sum", numeric_only=True)

    if ranking_choice == "Most Frequent Crash Locations":
        ranking = ranking.sort_values(by='COUNT', ascending=False)[["COUNT"]].head(10)
    elif ranking_choice == "Most Frequent Crash Locations + Weighted":
        ranking = ranking.sort_values(by='INJURY_SCORE', ascending=False)[['INJURIES_FATAL',
       'INJURIES_INCAPACITATING', 'INJURIES_NON_INCAPACITATING', "COUNT","INJURY_SCORE"]].head(10)
    elif ranking_choice == "Most Dangerous Crash Locations":
        ranking["Average Injury Score"] = ranking["INJURY_SCORE"] / ranking["COUNT"]
        ranking = ranking.sort_values(by='INJURY_SCORE', ascending=False)[['INJURIES_FATAL',
       'INJURIES_INCAPACITATING', 'INJURIES_NON_INCAPACITATING', "COUNT","INJURY_SCORE", "Average Injury Score"]].head(10)
    ranking["CRASHES PER YEAR"] = ranking["COUNT"]/9
    
    # Create "PER YEAR" columns by dividing by 9
    ranking["CRASHES PER YEAR"] = ranking["COUNT"] / 9
    ranking["FATALS PER YEAR"] = ranking["INJURIES_FATAL"] / 9
    ranking["INCAPACITATING INJURIES PER YEAR"] = ranking["INJURIES_INCAPACITATING"] / 9
    ranking["NON-INCAPACITATING INJURIES PER YEAR"] = ranking["INJURIES_NON_INCAPACITATING"] / 9
    ranking["INJURY SCORE PER YEAR"] = ranking["INJURY_SCORE"] / 9

    # Optional: display only the "PER YEAR" columns
    ranking_per_year = ranking[[
        "CRASHES PER YEAR",
        "FATALS PER YEAR",
        "INCAPACITATING INJURIES PER YEAR",
        "NON-INCAPACITATING INJURIES PER YEAR",
        "INJURY SCORE PER YEAR"
    ]]

    st.dataframe(ranking_per_year)
    