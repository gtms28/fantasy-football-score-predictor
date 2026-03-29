import pandas as pd

def quarterback():
    df_pass = pd.read_csv("ScorePredictorPassYds.csv")
    df_pass.head(50)
    df_pass.size
    df_rush_qb = pd.read_csv("ScorePredictorRushYdsQB.csv")
    df_rush_qb.head(30)
    df_merged = pd.merge(df_pass, df_rush_qb, left_on="Player", right_on="Player", how="inner")
    df_merged.head(50)
    df_merged["PassAtt"] = df_merged["Att_x"]
    df_merged["RushAtt"] = df_merged["Att_y"]
    df_merged["PassYds"] = df_merged["Yds_x"]
    df_merged["PassTD"] = df_merged["TD_x"]
    df_merged["RushYds"] = df_merged["Yds_y"]
    df_merged["RushTD"] = df_merged["TD_y"]
    df_merged["PassY/A"] = df_merged["Y/A_x"]
    df_merged["RushY/A"] = df_merged["Y/A_y"]
    df_merged = df_merged[["Player", "Team", "G", "Cmp", "PassAtt", "PassYds", "PassTD", "Int", "PassY/A", "PassRtg", "QBR", "RushAtt", "RushYds", "RushTD", "RushY/A", "Y/G"]]
    df_merged.head(50)
    df_merged = df_merged.dropna()
    df_merged.head(50)
    total_fpts = (df_merged['PassYds'].astype("int")/25 + df_merged['PassTD'].astype("int") * 4 + df_merged['Int'].astype("int") * -2 + df_merged['RushYds'].astype("int")/10 + df_merged['RushTD'].astype("int") * 6)
    fpts_g = total_fpts / df_merged['G'].astype("int")
    fpts_g.round(2)
    df_merged["FPTS/G"] = fpts_g
    df_merged.head(50)
    df_pass_yds_allowed = pd.read_csv("PassYdsAllowed.csv")
    df_pass_yds_allowed.head(32)
    qb_name = input("Enter QB Name: ")
    qb_opponent = input(f"Who is {qb_name} playing against? ")
    opponent_rtg = (df_pass_yds_allowed[df_pass_yds_allowed['Team'] == qb_opponent]['RTG'])
    rtg_mult = (opponent_rtg/90)**2
    fpts_g = (df_merged[df_merged['Player'] == qb_name]['FPTS/G'])
    qb_fpts = fpts_g.iloc[0] * rtg_mult.iloc[0]
    injury = input(f"Does {qb_name} have an injury? (Y/N) ")
    if injury == "Y":
      injury_type = input(f"""\nSelect {qb_name}'s injury status:
      P - Probable
      Q - Questionable
      D - Doubtful
      O - Out\n""")
      if injury_type == "O":
        fpts_g_round = qb_fpts * 0
        print(f"Projected Fantasy Points: {round(fpts_g_round, 2)}")
      elif injury_type == "Q":
        fpts_g_round = qb_fpts * 0.8
        print(f"Projected Fantasy Points: {round(fpts_g_round, 2)}")
      elif injury_type == "D":
        fpts_g_round = qb_fpts * 0
        print(f"Projected Fantasy Points: {round(fpts_g_round, 2)}")
      elif injury_type == "P":
        fpts_g_round = qb_fpts
        print(f"Projected Fantasy Points: {round(fpts_g_round, 2)}")
    elif injury == "N":
        fpts_g_round = qb_fpts
        print(f"Projected Fantasy Points: {round(fpts_g_round, 2)}")

def runningback():
    df_rush = pd.read_csv("ScorePredictorRushYds.csv")
    df_rush.head(50)
    df_rec_rb = pd.read_csv("ScorePredictorRecYdsRB.csv")
    df_rec_rb.head(50)
    df_merged = pd.merge(df_rush, df_rec_rb, left_on="Player", right_on="Player", how="inner")
    df_merged.head(50)
    df_merged["Team"] = df_merged["Team_x"]
    df_merged["RushYds"] = df_merged["Yds_x"]
    df_merged["RushTD"] = df_merged["TD_x"]
    df_merged["RecYds"] = df_merged["Yds_y"]
    df_merged["RecTD"] = df_merged["TD_y"]
    df_merged[["Player", "Team", "G", "Att", "RushYds", "RushTD", "AVG", "Tgt",	"Rec",	"RecYds",	"RecTD"]]
    df_rush.head(100)
    df_rec_rb = pd.read_csv("ScorePredictorRecYdsRB.csv")
    df_rec_rb.head(50)
    df_merged = pd.merge(df_rush, df_rec_rb, left_on="Player", right_on="Player", how="inner")
    df_merged.head(100)
    df_merged["Team"] = df_merged["Team_x"]
    df_merged["RushYds"] = df_merged["Yds_x"]
    df_merged["RushTD"] = df_merged["TD_x"]
    df_merged["RecYds"] = df_merged["Yds_y"]
    df_merged["RecTD"] = df_merged["TD_y"]
    df_merged[["Player", "Team", "G", "Att", "RushYds", "RushTD", "AVG", "Tgt",	"Rec",	"RecYds",	"RecTD"]]
    total_fpts = (df_merged['RushYds'].astype("int")/10 + df_merged['RushTD'].astype("int") * 6 + df_merged['Rec'].astype("int") * 1 + df_merged['RecYds'].astype("int")/10 + df_merged['RecTD'].astype("int") * 6)
    fpts_g = total_fpts / df_merged['G'].astype("int")
    fpts_g.round(2)
    df_merged["FPTS/G"] = fpts_g
    df_yds_allowed = pd.read_csv("RushYdsAllowed.csv")
    opponent_rush_yds = df_yds_allowed['Rush Yds']
    opponent_rush_tds = df_yds_allowed['TD']
    fpts_g_allowed = ((opponent_rush_yds / 10) + (opponent_rush_tds * 6))/17
    df_yds_allowed["FPTS/G"] = fpts_g_allowed
    rb_name = input("Enter RB name: ")
    rb_opponent = input(f"Who is {rb_name} playing against? ")
    opponent_fpts_g = (df_yds_allowed[df_yds_allowed['Team'] == rb_opponent]['FPTS/G'])
    rush_mult = (opponent_fpts_g/16)**0.5
    avg_fpts = df_merged[df_merged['Player'] == rb_name]['FPTS/G'].dropna().astype(float)
    rb_fpts = avg_fpts.iloc[0] * rush_mult.iloc[0]
    injury = input(f"Does {rb_name} have an injury? (Y/N) ")
    if injury == "Y":
      injury_type = input(f"""\nSelect {rb_name}'s injury status:
      P - Probable
      Q - Questionable
      D - Doubtful
      O - Out\n""")
      if injury_type == "O":
        rb_fpts_round = rb_fpts * 0
        print(f"Projected Fantasy Points: {round(rb_fpts_round, 2)}")
      elif injury_type == "Q":
        rb_fpts_round = rb_fpts * 0.8
        print(f"Projected Fantasy Points: {round(rb_fpts_round, 2)}")
      elif injury_type == "D":
        rb_fpts_round = rb_fpts * 0
        print(f"Projected Fantasy Points: {round(rb_fpts_round, 2)}")
      elif injury_type == "P":
        rb_fpts_round = rb_fpts
        print(f"Projected Fantasy Points: {round(rb_fpts_round, 2)}")
    elif injury == "N":
        print(f"Projected Fantasy Points: {round(rb_fpts, 2)}")


def widereceiver():
    df_rec = pd.read_csv("ScorePredictorRecYds.csv")
    print(df_rec)
    df_rec['Name'].str[-3:]
    df_rec['Name'].str[-6:]
    df_rec['Name'].str[-3:].str.isupper()
    df_rec['Name'].str[-3:].str.isupper().head(10)
    df_rec[df_rec['Name'].str[-3:].str.isupper() == False]
    df_rec[df_rec['Name'].str[-3:].str.isupper() == False]['Name']
    df_rec[df_rec['Name'].str[-3:].str.isupper() == False]['Name'].str[-2:]
    in_progress = df_rec[df_rec['Name'].str[-3:].str.isupper() == True]
    in_progress.head(20)
    in_progress[in_progress['Name'].str[-4:].str.isupper() == False]
    in_progress = in_progress[in_progress['Name'].str[-4:].str.isupper() == True]
    in_progress.head(20)
    in_progress['Name'].str[-4]=="."
    in_progress = in_progress[df_rec['Name'].str[-5:].str.isupper() == True]
    in_progress.head(20)
    in_progress = in_progress[df_rec['Name'].str[-6:].str.isupper() == True]
    in_progress.head(20)
    def lowercase_at_index(column_values, index):
      return column_values.str[index].str.isupper() == False
    unsorted_df = df_rec.copy()
    unsorted_df.head(10)
    unsorted_df['Team'].isna().head(10)
    lowercase_at_index(unsorted_df['Name'], -3).head(10)
    mask = lowercase_at_index(unsorted_df['Name'], -3) & unsorted_df['Team'].isna()
    mask.head(10)
    two_letter_team_names = unsorted_df[mask]
    two_letter_team_names.head()
    unsorted_df = unsorted_df[~mask]
    unsorted_df.head()
    def lowercase_at_index(player_names, index):
      return player_names.str[index].str.isupper() == False
    def team_starts_at(player_names, current_team, index):
      return lowercase_at_index(player_names, index-1) & current_team.isna()
    unsorted_df = df_rec.copy()
    unsorted_df['Team'] = unsorted_df['Team'].astype('string')
    unsorted_df.head()
    # in order to know if a players team starts at some given index
    # two things must be true: the index before it should be lowercase
    # and also, they shouldn't already have a team
    # this prevents duplication when looking for 3 letter team names
    # as a players last name 4 letters from the end would still be lowercase
    # eg: SmithLV has lowercase both at -3 and -4
    # but once their team is assigned, they will not be checked for lowercase at -4
    mask = team_starts_at(unsorted_df['Name'], unsorted_df['Team'], -2)
    unsorted_df.loc[mask, 'Team'] = unsorted_df.loc[mask, 'Name'].str[-2:]
    unsorted_df.loc[mask, 'Name'] = unsorted_df.loc[mask, 'Name'].str[:-2]
    unsorted_df.head(10)
    unsorted_df[~unsorted_df['Team'].isna()]
    mask = team_starts_at(unsorted_df['Name'], unsorted_df['Team'], -3)
    unsorted_df.loc[mask, 'Team'] = unsorted_df.loc[mask, 'Name'].str[-3:]
    unsorted_df.loc[mask, 'Name'] = unsorted_df.loc[mask, 'Name'].str[:-3]
    unsorted_df.head(10)
    mask = unsorted_df['Team'].isna()
    unsorted_df.loc[mask, 'Team'] = unsorted_df.loc[mask, 'Name'].str[-3:]
    unsorted_df.loc[mask, 'Name'] = unsorted_df.loc[mask, 'Name'].str[:-3]
    unsorted_df.head(10)
    unsorted_df[unsorted_df['Team'].isna()]
    unsorted_df.head(20)
    #find each player's total fpts and divide by games played
    unsorted_df['YDS'].str.replace(",", "").astype("int")
    total_fpts = (unsorted_df['YDS'].str.replace(",", "").astype("int"))/10 + (unsorted_df['TD'].astype("int"))*6 + unsorted_df['REC'].astype("int")
    total_fpts.head(10)
    fpts_per_game = total_fpts/(unsorted_df['GP'])
    fpts_per_game.head(20)
    unsorted_df["FPTS/G"] = total_fpts/(unsorted_df['GP'])
    unsorted_df.head(10)
    df_yds_allowed = pd.read_csv("PassYdsAllowed.csv")
    df_yds_allowed.head(20)
    wr_name = input("Enter WR Name: ")
    wr_opponent = input(f"Who is {wr_name} playing against? ")
    opponent_rtg = (df_yds_allowed[df_yds_allowed['Team'] == wr_opponent]['RTG'])
    opponent_rtg
    # (unsorted_df[unsorted_df['Name'] == wr_name]['FPTS/G'])
    rtg_mult = (opponent_rtg/90)**2
    avg_fpts = (unsorted_df[unsorted_df['Name'] == wr_name]['FPTS/G'])
    wr_fpts = avg_fpts.iloc[0] * rtg_mult.iloc[0]
    injury = input(f"Does {wr_name} have an injury? (Y/N) ")
    if injury == "Y":
      injury_type = input(f"""\nSelect {wr_name}'s injury status:
      P - Probable
      Q - Questionable
      D - Doubtful
      O - Out\n""")
      if injury_type == "O":
        avg_fpts_round = wr_fpts * 0
        print(f"Projected Fantasy Points: {round(avg_fpts_round, 2)}")
      elif injury_type == "Q":
        avg_fpts_round = wr_fpts * 0.8
        print(f"Projected Fantasy Points: {round(avg_fpts_round, 2)}")
      elif injury_type == "D":
        avg_fpts_round = wr_fpts * 0
        print(f"Projected Fantasy Points: {round(avg_fpts_round, 2)}")
      elif injury_type == "P":
        avg_fpts_round = wr_fpts
        print(f"Projected Fantasy Points: {round(avg_fpts_round, 2)}")
    elif injury == "N":
        avg_fpts_round = wr_fpts
        print(f"Projected Fantasy Points: {round(avg_fpts_round, 2)}")

def calculator():
    print("Welcome To Gautam's Fantasy Score Calculator!")
    print("Scoring System: ESPN Standard")
    ppr = input("\n\nIs your league PPR (points per reception)? (Y/N) ")
    print("\n\nPassing")
    pass_yds = int(input("Passing Yards: "))
    pass_tds = int(input("Passing Touchdowns: "))
    ints = int(input("Interceptions: "))
    print("\n\nRushing")
    rush_yds = int(input("Rushing Yards: "))
    rush_tds = int(input("Rushing Touchdowns: "))
    fumbles = int(input("Fumbles Lost: "))
    print("\n\nReceiving")
    if ppr == "Y":
      recs = int(input("Receptions: "))
    rec_yds = int(input("Receiving Yards: "))
    rec_tds = int(input("Receiving Touchdowns: "))
    print("\n\nKicking")
    short_fgs = int(input("0-39 Yard Field Goals: "))
    fgs_40 = int(input("40-49 Yard Field Goals: "))
    fgs_50 = int(input("50-59 Yard Field Goals: "))
    fgs_60 = int(input("60+ Yard Field Goals: "))
    missed_fgs = int(input("Missed Field Goals: "))
    xpm = int(input("Extra Points Made: "))
    print("\n\nOther")
    long_tds = int(input("50+ Yard Touchdowns: "))
    conv_2pt = int(input("2-Point Conversions: "))
    total_offense = (pass_yds * 0.04) + (pass_tds * 4) + (ints * -2) + (fumbles * -2) + (rush_yds * 0.1) + (rush_tds * 6) + (long_tds * 1) + (conv_2pt * 2) + (recs * 1) + (rec_yds * 0.1) + (rec_tds * 6) + (short_fgs * 3) + (fgs_40 * 4) + (fgs_50 * 5) + (fgs_60 * 6) + (missed_fgs * -1) +(xpm * 1)
    print("\n\nTotal Fantasy Score: " + str(total_offense))

