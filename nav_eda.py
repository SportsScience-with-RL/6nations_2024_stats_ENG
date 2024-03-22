import streamlit as st

from functions.data_functions import *

# @st.partial
def eda_navigation(data_6nations, teams_img, games_scores, games_results, tbl_desc_full, tbl_desc_period):
    c1, _, c2 = st.columns([.2, .05, .75])
    with c1:
        st.write('')
        team_sel = st.selectbox('Select a team', sorted(list(teams_img.keys())))
        data_team = data_6nations[data_6nations['Match'].str.contains(team_sel)].reset_index(drop=True).copy()
        _, c11 = st.columns([.25, .75])
        with c11:
            st.image(teams_img[team_sel])
    
    with c2:
        st.title('Results')
        c22= st.columns(5)
        for (g, s), c in zip(games_scores[team_sel].items(), c22):
            c.markdown(g)
            if games_results[team_sel][g] == 'V':
                c.markdown(f':green[{s}]')
            elif games_results[team_sel][g] == 'D':
                c.markdown(f':red[{s}]')
            else:
                c.markdown(f':orange[{s}]')
    st.write('---')

    st.header('Games Timelines')
    c_timeline = [column for row in [st.columns(2) for _ in range(2)] for column in row]
    for i, r in enumerate(['R1', 'R2', 'R3', 'R4']):
        with c_timeline[i]:
            data_team_r1 = data_team[data_team['Round']==r].reset_index(drop=True).copy()
            game_ = data_team_r1['Match'].unique()[0]
            st.image(f'eda_timeline/{r}_{game_}.png')
    c_r5 = st.columns([.2, .6, .2])
    with c_r5[1]:
        data_team_r5 = data_team[data_team['Round']=='R5'].reset_index(drop=True).copy()
        game_ = data_team_r5['Match'].unique()[0]
        st.image(f'eda_timeline/R5_{game_}.png')

    st.write('')

    st.header('Distributions')
    st.subheader('Boxplots (without outliers)')
    c_box = [column for row in [st.columns(3) for _ in range(3)] for column in row]
    for i, m in enumerate(['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']):
        with c_box[i]:
            st.image(f'eda_boxplots/{team_sel}_{m}.png')
    st.write('')

    st.subheader('Descriptive Tables')
    with st.expander('**:blue[Full games]**'):
        for m in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
            st.caption(m)
            st.dataframe(tbl_desc_full[(tbl_desc_full['game'].str.contains(team_sel)) 
                                       & (tbl_desc_full['metric']==m)].drop(columns=['game', 'metric']), use_container_width=True)
    with st.expander('**:blue[Full games by 20min periods split]**'):
        for m in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
            st.caption(m)
            st.dataframe(tbl_desc_period[(tbl_desc_period['game'].str.contains(team_sel)) 
                                         & (tbl_desc_period['metric']==m)].drop(columns=['game', 'metric']), use_container_width=True)
    st.write('')
    st.write('---')
    
    st.header('Progression (median number of zones) according to starting zone of the sequences')
    data_team_r1 = data_team[data_team['Round']=='R1'].reset_index(drop=True).copy()
    data_team_r2 = data_team[data_team['Round']=='R2'].reset_index(drop=True).copy()
    data_team_r3 = data_team[data_team['Round']=='R3'].reset_index(drop=True).copy()
    data_team_r4 = data_team[data_team['Round']=='R4'].reset_index(drop=True).copy()
    data_team_r5 = data_team[data_team['Round']=='R5'].reset_index(drop=True).copy()
    
    game_r1 = data_team_r1['Match'].unique()[0]
    game_r2 = data_team_r2['Match'].unique()[0]
    game_r3 = data_team_r3['Match'].unique()[0]
    game_r4 = data_team_r4['Match'].unique()[0]
    game_r5 = data_team_r5['Match'].unique()[0]

    st.subheader(f'**:blue[{game_r1}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r1.split(' - ')[0])
        st.image(f"eda_fields/R1_{game_r1.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/R1_0'-20'_{game_r1.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R1_40'-60'_{game_r1.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/R1_20'-40'_{game_r1.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R1_60'-80'_{game_r1.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r1.split(' - ')[1])
        st.image(f"eda_fields/R1_{game_r1.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/R1_0'-20'_{game_r1.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R1_40'-60'_{game_r1.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/R1_20'-40'_{game_r1.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R1_60'-80'_{game_r1.split(' - ')[1]}.png")

    st.subheader(f'**:blue[{game_r2}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r2.split(' - ')[0])
        st.image(f"eda_fields/R2_{game_r2.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/R2_0'-20'_{game_r2.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R2_40'-60'_{game_r2.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/R2_20'-40'_{game_r2.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R2_60'-80'_{game_r2.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r2.split(' - ')[1])
        st.image(f"eda_fields/R2_{game_r2.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/R2_0'-20'_{game_r2.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R2_40'-60'_{game_r2.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/R2_20'-40'_{game_r2.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R2_60'-80'_{game_r3.split(' - ')[1]}.png")

    st.subheader(f'**:blue[{game_r3}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r3.split(' - ')[0])
        st.image(f"eda_fields/R3_{game_r3.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/R3_0'-20'_{game_r3.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R3_40'-60'_{game_r3.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/R3_20'-40'_{game_r3.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R3_60'-80'_{game_r3.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r3.split(' - ')[1])
        st.image(f"eda_fields/R3_{game_r3.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/R3_0'-20'_{game_r3.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R3_40'-60'_{game_r3.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/R3_20'-40'_{game_r3.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R3_60'-80'_{game_r3.split(' - ')[1]}.png")
            
    st.subheader(f'**:blue[{game_r4}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r4.split(' - ')[0])
        st.image(f"eda_fields/R4_{game_r4.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/R4_0'-20'_{game_r4.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R4_40'-60'_{game_r4.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/R4_20'-40'_{game_r4.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R4_60'-80'_{game_r4.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r4.split(' - ')[1])
        st.image(f"eda_fields/R4_{game_r4.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/R4_0'-20'_{game_r4.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R4_40'-60'_{game_r4.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/R4_20'-40'_{game_r4.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R4_60'-80'_{game_r4.split(' - ')[1]}.png")

    st.subheader(f'**:blue[{game_r5}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r5.split(' - ')[0])
        st.image(f"eda_fields/R5_{game_r5.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/R5_0'-20'_{game_r5.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R5_40'-60'_{game_r5.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/R5_20'-40'_{game_r5.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R5_60'-80'_{game_r5.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r5.split(' - ')[1])
        st.image(f"eda_fields/R5_{game_r5.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/R5_0'-20'_{game_r5.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/R5_40'-60'_{game_r5.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/R5_20'-40'_{game_r5.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/R5_60'-80'_{game_r5.split(' - ')[1]}.png")