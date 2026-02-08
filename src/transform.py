import pandas as pd
# Extract
from src.extract import extract_raw_ball_data
balls=extract_raw_ball_data()
# Batting
Runs=balls.groupby(["ID","batter"])["batsman_run"].sum().reset_index().rename(columns={"batsman_run":"Batsman_Runs"})
balls_count=balls[~balls["extra_type"].isin(["wides"])]
Balls=balls_count.groupby(["ID","batter"])["batsman_run"].count().reset_index().rename(columns={"batsman_run":"Balls"})
Fours=balls[balls["batsman_run"]==4].groupby(["ID","batter"])["batsman_run"].count().reset_index().rename(columns={"batsman_run":"Fours"})
Sixes=balls[balls["batsman_run"]==6].groupby(["ID","batter"])["batsman_run"].count().reset_index().rename(columns={"batsman_run":"Sixes"})
Batting=Runs.merge(Balls,on=["ID","batter"],how="left").merge(Fours,on=["ID","batter"],how="left").merge(Sixes,on=["ID","batter"],how="left")
Batting.fillna(0,inplace=True)
Batting["Strike_Rate"]=Batting["Batsman_Runs"]/Batting["Balls"]*100
def Batting_Score(row):
    score=row["Batsman_Runs"]
    score=score+(4*row["Fours"])+(6*row["Sixes"])
    if row["Batsman_Runs"]>25 and row["Batsman_Runs"]< 50:
        score=score+4
    elif  row["Batsman_Runs"]>=50 and row["Batsman_Runs"]< 75:
        score=score+8+4
    elif  row["Batsman_Runs"]>=75 and row["Batsman_Runs"]< 100:
        score=score+12+8+4
    elif row["Batsman_Runs"]>=100:
        score=score+16+12+8+4
    elif row["Batsman_Runs"]==0:
        score=score-2
    elif row["Balls"]>=10:
        if row["Strike_Rate"]>=170:
            score=score+6
        elif row["Strike_Rate"]>150.01 and row["Strike_Rate"]<170:
            score=score+4
        elif row["Strike_Rate"]>130 and row["Strike_Rate"]<150:
            score=score+2
        elif row["Strike_Rate"]>60 and row["Strike_Rate"]<70:
            score=score-2
        elif row["Strike_Rate"]>50 and row["Strike_Rate"]<59.99:
            score=score-4
        elif row["Strike_Rate"]<50:
            score=score-6
    return score
Batting["Bat_Score"]=Batting.apply(Batting_Score,axis=1)
Batting=Batting[["ID","batter","Bat_Score"]]
# Bowling
Runs_conceded=balls.groupby(["ID","bowler"])["total_run"].sum().reset_index(name="runs_conceded")
dot_balls = (
    balls[balls["total_run"] == 0]
    .groupby(["ID", "bowler"])
    .size()
    .reset_index(name="dot_balls")
)
wickets = (
    balls[(balls["isWicketDelivery"] == 1) & (balls["kind"] != "run out")]
    .groupby(["ID", "bowler"])
    .size()
    .reset_index(name="wickets")
)
over_runs = (
    balls.groupby(["ID", "bowler", "overs"])["total_run"]
      .sum()
      .reset_index(name="over_runs")
)
maidens = (
    over_runs[over_runs["over_runs"] == 0]
    .groupby(["ID", "bowler"])
    .size()
    .reset_index(name="maidens")
)
balls_bowled=balls[~balls["extra_type"].isin(["wides", "noballs","penalty"])].groupby(["ID","bowler"]).size().reset_index(name="balls_bowled")
Bowled_lbw = (
    balls[
        (balls["isWicketDelivery"] == 1) &
        (balls["kind"].isin(['bowled', "lbw"]))
    ]
    .groupby(["ID","bowler"])
    .size()
    .reset_index(name="wickets_bowled_lbw")
)
Bowling=Runs_conceded.merge(balls_bowled,on=["ID","bowler"],how="left").merge(dot_balls,on=["ID","bowler"],how="left").merge(wickets,on=["ID","bowler"],how="left")
Bowling=Bowling.merge(maidens,on=["ID","bowler"],how="left")
Bowling=Bowling.merge(Bowled_lbw,on=["ID","bowler"],how="left")
Bowling.fillna(0,inplace=True)
Bowling.rename(columns={"wickets_bowled_lbw":"Bowled/lbw"},inplace=True)
Bowling["Economy"]=(Bowling["runs_conceded"]/Bowling["balls_bowled"])*6
def Bowling_score(row):
    score=0
    score=score+row["dot_balls"]+(30*row["wickets"]) + (8*row["Bowled/lbw"]) +(12*row["maidens"])
    if row["wickets"]>=3:
        score=score+4
    elif row["wickets"]>=4:
        score=score+8
    elif row["wickets"]>=5:
        score=score+12
    elif row["balls_bowled"]>=12:
        if row["Economy"]<5:
            score=score+6
        elif row["Economy"]>=5 and row["Economy"]<5.99:
            score=score+4
        elif row["Economy"]>6 and row["Economy"]<7:
            score=score+2
        elif row["Economy"]>10 and row["Economy"]<11:
            score=score-2
        elif row["Economy"]>11.01 and row["Economy"]<12:
            score=score-4
        elif row["Economy"]>12:
            score=score-6
    return score 
Bowling["Bowling_Score"]=Bowling.apply(Bowling_score,axis=1)
Bowling=Bowling[["ID","bowler","Bowling_Score"]]
# Fielding
Catch_Run_out=balls[balls["kind"].isin(['caught','run out','stumped'])]
Catch=Catch_Run_out[Catch_Run_out["kind"]=="caught"]
Catch=Catch_Run_out[Catch_Run_out["kind"]=="caught"].groupby(["ID","fielders_involved"])["isWicketDelivery"].sum().reset_index(name="Catches")
Stumping=Catch_Run_out[Catch_Run_out["kind"]=="stumped"].groupby(["ID","fielders_involved"])["isWicketDelivery"].sum().reset_index(name="Stumping")
Run_out=Catch_Run_out[Catch_Run_out["kind"]=="run out"].groupby(["ID","fielders_involved"])["isWicketDelivery"].sum().reset_index(name="Run_out")
Fielding=Catch.merge(Stumping, on =["ID","fielders_involved"],how="outer").merge(Run_out,on =["ID","fielders_involved"],how="outer")
Fielding.fillna(0,inplace=True)
def Fielding_Score(row):
    score=0
    score=(8*row["Catches"])+(12*row["Stumping"])+(12*row["Run_out"])
    if row["Catches"]>=3:
        score=score+4
    return score
Fielding["Fielding_Score"]=Fielding.apply(Fielding_Score,axis=1)
# Merging Batting, Bowling and Fielding
Batting_Bowling=pd.merge(Batting,Bowling,left_on=["ID","batter"],right_on=["ID","bowler"],how="outer")
Batting_Bowling_Fielding=pd.merge(Batting_Bowling,Fielding,left_on=["ID","batter"],right_on=["ID","fielders_involved"],how="outer")
Batting_Bowling_Fielding["Player"]=Batting_Bowling_Fielding["batter"].combine_first(Batting_Bowling_Fielding["bowler"])
Batting_Bowling_Fielding["Players"]=Batting_Bowling_Fielding["Player"].combine_first(Batting_Bowling_Fielding["fielders_involved"])
Players=Batting_Bowling_Fielding.drop(columns=["batter","bowler","fielders_involved","Player"])
Players=Players[["ID","Players","Bat_Score","Bowling_Score","Fielding_Score"]].fillna(0)
# Final Score
Players["Score"]=Players["Bat_Score"]+Players["Bowling_Score"]+Players["Fielding_Score"]
Players
# Load
from src.load import load_dream11_points
load_dream11_points(Players)




    