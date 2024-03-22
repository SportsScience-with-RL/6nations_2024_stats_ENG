import streamlit as st
from streamlit_option_menu import option_menu
from io import StringIO
import pandas as pd

def stat_navigation(data_6nations, teams_img, games_scores, games_results, tbl_ttest, tbl_ttest_period, tbl_anova, tbl_anova_period):
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
            c.markdown(f'''**{g}**''')
            if games_results[team_sel][g] == 'V':
                c.markdown(f':green[{s}]')
            elif games_results[team_sel][g] == 'D':
                c.markdown(f':red[{s}]')
            else:
                c.markdown(f':orange[{s}]')
    st.write('---')
    st.write('---')
    st.header('Frequentist approach')
    st.write('')

    stat_menu = option_menu(menu_title='',
                            options=['Games comparison', "Team comparison"],
                            icons=['copy', 'person-bounding-box'],
                            default_index=0, orientation='horizontal')
    
    if stat_menu == 'Games comparison':
        with st.expander('Approach'):
            st.subheader('**:blue[Two teams comparison for the all game]**')
            st.write("""A Shapiro-Wilk test is performed for each team to test the null hypothesis that the values of the variable are normally distributed.
                     A Levene test is also carried out in order to test the null hypothesis of homogeneity of variances between the two teams for the chosen variable.""")
            st.write("""For a p-value of the Shapiro-Wilk test below the 95% threshold, we reject the null hypothesis: the team variable does not seem to follow a normal distribution.
                     For a p value of the Levene test lower than the 95% threshold, we reject the null hypothesis: we assume the absence of homogeneity of variances (homoscedasticity) between the two teams for the chosen variable.""")
            st.write("For a p value > 0.05 in the Shapiro-Wilk test and Levene test, we will perform a Student's t-test for independent samples.")
            st.write("For a p value > 0.05 for the Shapiro-Wilk test and < 0.05 for the Levene test, we will perform a Welch test.")
            st.write("For a p value < 0.05 in the Shapiro-Wilk test, we will perform a Mann-Whitney U test.")
        st.write('---')

        
        for game in data_team['Match'].unique():
            st.subheader(game)
            if st.toggle('Statistic Results', key=game):
                stats_tabs = st.tabs(['Game', '20min Periods'])
                with stats_tabs[0]:
                    c_box = [column for row in [st.columns(3) for _ in range(2)] for column in row]

                    for i, m in enumerate(['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']):
                        with c_box[i]:
                            st.image(f'stat_boxplots/{game}_{m}.png')
                            st.write(tbl_ttest.loc[(tbl_ttest['Match']==game) & (tbl_ttest['Metric']==m), 'Résultat'].unique()[0])
                            st.write('')
                with stats_tabs[1]:
                    for m in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
                        st.markdown(f'**{m}**')
                        c_box = st.columns(4)
                        with c_box[0]:
                            st.caption("0'-20'")
                            st.image(f"stat_boxplots_period/{game}_0'-20'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="0'-20'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
                        with c_box[1]:
                            st.caption("20'-40'")
                            st.image(f"stat_boxplots_period/{game}_20'-40'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="20'-40'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
                        with c_box[2]:
                            st.caption("40'-60'")
                            st.image(f"stat_boxplots_period/{game}_40'-60'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="40'-60'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
                        with c_box[3]:
                            st.caption("60'-80'")
                            st.image(f"stat_boxplots_period/{game}_60'-80'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="60'-80'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
            st.write('---')

    elif stat_menu == "Team comparison":
        with st.expander('Approach'):
            st.subheader('**:blue[Two teams comparison for each 20min period for each game]**')
            st.write("""A Shapiro-Wilk test is performed for each team period to test the null hypothesis that the values of the variable for each game/period are normally distributed.
              A Levene test is also carried out in order to test the null hypothesis of homogeneity of variances between games/periods for the chosen variable.""")
            st.write("""For a p-value of the Shapiro-Wilk test below the 95% threshold, we reject the null hypothesis: the variable does not seem to follow a normal distribution for the game/period.
                     For a p-value of the Levene test lower than the 95% threshold, we reject the null hypothesis: we assume the absence of homogeneity of variances (homoscedasticity) between games/periods for the chosen variable.""")
            st.write('')
            st.write("For a p value > 0.05 in the Shapiro-Wilk test and Levene test, we will carry out a one-way ANOVA, in order to test the null hypothesis according to which the means of the games/periods variable are equal.")
            st.write("For a p value < 0.05 in the Shapiro-Wilk test, we will perform a Kruskall-Wallis test, in order to test the null hypothesis according to which the distribution of the variable is the same for all games/periods.")
            st.write("""For an ANOVA p-value below the 95% threshold, we reject the null hypothesis: the average of at least one period is different from one other game/period (at least).
                     In this case a post-hoc Tukey test is carried out in order to test all the comparison combinations of the different games/periods.
                     A p value < 0.05 in the Tukey test suggests a statistically significant difference between the two games/periods.""")
            st.write("""For a p-value of the Kruskall-Wallis test below the 95% threshold, we reject the null hypothesis: the distribution of at least one period is different from one other game/period (at least).
                     In this case a post-hoc Conover test is carried out in order to test all the comparison combinations of the different games/periods.
                     A p-value < 0.05 in the Conover test suggests a statistically significant difference between the two games/periods.""")
            st.write("""For each significant post-hoc test, Cohen's d is calculated to characterize the effect size.
                     The greater the absolute value of d, the greater the size of the effect (the difference is greater between games/periods).
                     The sign of d (positive or negative) indicates the direction of the difference between games/periods.""")
            st.write("For more information on the interpretation of Cohen's d, go to the following link: [https://rpsychologist.com/fr/cohend/](https://rpsychologist.com/fr/cohend/)")
        
        st.subheader('Games Comparison')
        stats_tabs = st.tabs(['Games', '20min Periods'])
        with stats_tabs[0]:
            c_box = [column for row in [st.columns(3) for _ in range(2)] for column in row]
            for i, m in enumerate(['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']):
                with c_box[i]:
                    st.image(f'stat_anova_game/{team_sel}_{m}.png')
                    st.write('')
                    st.write(tbl_anova.loc[(tbl_anova['Team']==team_sel) & (tbl_anova['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova.loc[(tbl_anova['Team']==team_sel)
                                     & (tbl_anova['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.dataframe(pd.read_json(StringIO(tbl_anova.loc[(tbl_anova['Team']==team_sel)
                                                                        & (tbl_anova['Metric']==m), 'Post-hoc_res'].values[0])))
        with stats_tabs[1]:
            for m in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
                st.markdown(f'**{m}**')
                c_box = st.columns(4)
                with c_box[0]:
                    st.caption("0'-20'")
                    st.image(f"stat_anova_period/{team_sel}_0'-20'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="0'-20'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="0'-20'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="0'-20'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))
                with c_box[1]:
                    st.caption("20'-40'")
                    st.image(f"stat_anova_period/{team_sel}_20'-40'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="20'-40'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="20'-40'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="20'-40'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))
                with c_box[2]:
                    st.caption("40'-60'")
                    st.image(f"stat_anova_period/{team_sel}_40'-60'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="40'-60'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="40'-60'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="40'-60'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))
                with c_box[3]:
                    st.caption("60'-80'")
                    st.image(f"stat_anova_period/{team_sel}_60'-80'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="60'-80'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="60'-80'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="60'-80'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))