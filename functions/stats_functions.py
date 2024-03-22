import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp
import streamlit as st

def stat_report_ttest(data):
    tbl_comp = pd.DataFrame()

    for g in data['Match'].unique():
        data_g = data[data['Match']==g].copy()
    
        for metric in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
            team1_stat = data_g[metric][data_g['Possession']==g.split(' - ')[0]]
            team2_stat = data_g[metric][data_g['Possession']==g.split(' - ')[1]]

            #Normalité
            team1_shap_p = round(stats.shapiro(team1_stat).pvalue, 3)
            team2_shap_p = round(stats.shapiro(team2_stat).pvalue, 3)

            #Egalité variances
            lev_p = round(stats.levene(team1_stat, team2_stat, center='mean').pvalue, 3)

            if (team1_shap_p > .05) and (team2_shap_p > .05):
                if lev_p > .05:
                    ttest_ = stats.ttest_ind(team1_stat, team2_stat)
                    if ttest_.pvalue > 0.05:
                       res = f"""A Student t-test suggests that the difference is not statistically significant
                                (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)})."""
                    else:
                        res = f"""A Student t-test suggests that the difference is statistically significant
                                (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}*)."""
                elif lev_p < .05:
                    ttest_ = stats.ttest_ind(team1_stat, team2_stat, equal_var=False)
                    if ttest_.pvalue > 0.05:
                        res = f"""A Welch test suggests that the difference is not statistically significant
                                (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)})."""
                    else:
                        res = f"""A Welch test suggests that the difference is statistically significant 
                                (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}*)."""
            else:
                mann_ = stats.mannwhitneyu(team1_stat, team2_stat)
                if mann_.pvalue > 0.05:
                    res = f"""A Mann-Whitney U test suggests that the difference is not statistically significant 
                            (U={round(mann_.statistic, 2)}, p={round(mann_.pvalue, 2)})."""
                else:
                    res = f"""A Mann-Whitney U test suggests that the difference is statistically significant 
                            (U={round(mann_.statistic, 2)}, p={round(mann_.pvalue, 2)}*)."""
                
            tbl_m = pd.DataFrame([{'Match': g,
                                   'Metric': metric,
                                   'Résultat': res}])
            tbl_comp = pd.concat([tbl_comp, tbl_m], ignore_index=True)
        
    return tbl_comp

def stat_report_ttest_period(data):
    tbl_comp = pd.DataFrame()

    for g in data['Match'].unique():
        data_g = data[data['Match']==g].copy()

        for c in data_g['Chrono'].unique():
            data_g_c = data_g[data_g['Chrono']==c].copy()
            for metric in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
                team1_stat = data_g_c[metric][data_g_c['Possession']==g.split(' - ')[0]]
                team2_stat = data_g_c[metric][data_g_c['Possession']==g.split(' - ')[1]]

                if len(team1_stat) < 3 or len(team2_stat) <3:
                    res = "The number of data points from a period is short for testing"
                else:
                    #Normalité
                    team1_shap_p = round(stats.shapiro(team1_stat).pvalue, 3)
                    team2_shap_p = round(stats.shapiro(team2_stat).pvalue, 3)

                    #Egalité variances
                    lev_p = round(stats.levene(team1_stat, team2_stat, center='mean').pvalue, 3)

                    if (team1_shap_p > .05) and (team2_shap_p > .05):
                        if lev_p > .05:
                            ttest_ = stats.ttest_ind(team1_stat, team2_stat)
                            if ttest_.pvalue > 0.05:
                                res = f"""A Student t-test suggests that the difference is not statistically significant 
                                        (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)})."""
                            else:
                                res = f"""A Student t-test suggests that the difference is statistically significant 
                                        (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}*)."""
                        elif lev_p < .05:
                            ttest_ = stats.ttest_ind(team1_stat, team2_stat, equal_var=False)
                            if ttest_.pvalue > 0.05:
                                res = f"""A Welch test suggests that the difference is not statistically significant 
                                        (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)})."""
                            else:
                                res = f"""A Welch test suggests that the difference is statistically significant 
                                        (T={round(ttest_.statistic, 2)}, p={round(ttest_.pvalue, 2)}*)."""
                    else:
                        mann_ = stats.mannwhitneyu(team1_stat, team2_stat)
                        if mann_.pvalue > 0.05:
                            res = f"""A Mann-Whitney U test suggests that the difference is not statistically significant 
                                    (U={round(mann_.statistic, 2)}, p={round(mann_.pvalue, 2)})."""
                        else:
                            res = f"""A Mann-Whitney U test suggests that the difference is statistically significant 
                                    (U={round(mann_.statistic, 2)}, p={round(mann_.pvalue, 2)}*)."""
                        
                tbl_m = pd.DataFrame([{'Match': g,
                                       'Chrono': c,
                                       'Metric': metric,
                                       'Résultat': res}])
                tbl_comp = pd.concat([tbl_comp, tbl_m], ignore_index=True)
        
    return tbl_comp      

def cohen_d(x, y):
    n1, n2 = len(x), len(y)
    s1, s2 = np.var(x, ddof=1), np.var(y, ddof=1)
    s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    u1, u2 = np.mean(x), np.mean(y)
    return round((u1 - u2) / s, 3)


def stat_report_anova_game(data):
    order = ['R1', 'R2', 'R3', 'R4', 'R5']
    tbl_anova = pd.DataFrame()
    
    for t in data['Possession'].unique():
        data_t = data[data['Possession'].str.contains(t)].copy()

        for metric in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
            anova_groups = []
            shapiro_p = []

            for r in data_t['Round'].unique():
                data_r = data_t[data_t['Round']==r].copy()
                shap_p = round(stats.shapiro(data_r[metric]).pvalue, 3)
                shapiro_p.append(shap_p)
                anova_groups.append(data_r[metric])

            lev_p = round(stats.levene(*anova_groups, center='mean').pvalue, 3)
            normality_check = [s for s in shapiro_p if s > .05]

            if len(normality_check) == len(shapiro_p) and lev_p > .05:
                anova_ = stats.f_oneway(*anova_groups)
                if anova_.pvalue > 0.05:
                    res = f"""An ANOVA test suggests that the difference is not statistically significant between games/periods
                            (F={round(anova_.statistic, 2)}, p={round(anova_.pvalue, 2)})."""
                    res_ph = ""
                else:
                    res = f"""An ANOVA test suggests that the difference is statistically significant for at least one game/period
                            (F={round(anova_.statistic, 2)}, p={round(anova_.pvalue, 2)}*)."""
                    #Post-hoc
                    post_hoc_matrix = sp.posthoc_tukey(data_t, val_col=metric, group_col='Round')
                    post_hoc_matrix = post_hoc_matrix[order].reindex(order)

                    posthoc_res = pd.DataFrame(post_hoc_matrix.stack())
                    posthoc_res = posthoc_res.rename(columns={0: 'Tukey (p-value)'})
                    posthoc_res = round(posthoc_res, 3)
                    posthoc_res = posthoc_res[posthoc_res['Tukey (p-value)']<.05].copy()

                    for idx in posthoc_res.index:
                        posthoc_res.loc[idx, "Cohen's d"] = cohen_d(data_t[metric][data_t['Round']==idx[0]],
                                                                     data_t[metric][data_t['Round']==idx[1]])
                    
                    posthoc_res['d abs.'] = np.abs(posthoc_res["Cohen's d"])
                    posthoc_res = posthoc_res.drop_duplicates(subset='d abs.')

                    posthoc_res['Tukey (p-value)'] = ['< 0.05*' if p==0 else f'{p}*' if p<.05 else str(p) for p in posthoc_res['Tukey (p-value)']]
                    posthoc_res["Cohen's d"] = round(posthoc_res["Cohen's d"], 2)
                    posthoc_res = posthoc_res.drop(columns='d abs.')

                    if posthoc_res.empty:
                        res_ph = "The post-hoc test ultimately did not find a statistically significant difference."
                    else:
                        res_ph = posthoc_res.to_json()
            else:
                kruskal_ = stats.kruskal(*anova_groups)
                if kruskal_.pvalue < 0.05:
                    res = f"""A Kruskal-Wallis test suggests that the difference is statistically significant for at least one game/period
                            (F={round(kruskal_.statistic, 2)}, p={round(kruskal_.pvalue, 2)}*)."""
                    #Post-hoc
                    post_hoc_matrix = sp.posthoc_conover(data_t, val_col=metric, group_col='Round')
                    post_hoc_matrix = post_hoc_matrix[order].reindex(order)

                    posthoc_res = pd.DataFrame(post_hoc_matrix.stack())
                    posthoc_res = posthoc_res.rename(columns={0: 'Conover (p-value)'})
                    posthoc_res = round(posthoc_res, 3)
                    posthoc_res = posthoc_res[posthoc_res['Conover (p-value)']<.05].copy()
                    
                    for idx in posthoc_res.index:
                        posthoc_res.loc[idx, "Cohen's d"] = cohen_d(data_t[metric][data_t['Round']==idx[0]],
                                                                     data_t[metric][data_t['Round']==idx[1]])
                        
                    posthoc_res['d abs.'] = np.abs(posthoc_res["Cohen's d"])
                    posthoc_res = posthoc_res.drop_duplicates(subset='d abs.')

                    posthoc_res['Conover (p-value)'] = ['< 0.05*' if p==0 else f'{p}*' if p<.05 else str(p) for p in posthoc_res['Conover (p-value)']]
                    posthoc_res["Cohen's d"] = round(posthoc_res["Cohen's d"], 2)
                    posthoc_res = posthoc_res.drop(columns='d abs.')

                    if posthoc_res.empty:
                        res_ph = "The post-hoc test ultimately did not find a statistically significant difference."
                    else:
                        res_ph = posthoc_res.to_json()
                else:
                    res = f"""A Kruskal-Wallis test suggests that the difference is not statistically significant between games/periods 
                            (H={round(kruskal_.statistic, 2)}, p={round(kruskal_.pvalue, 2)})."""
                    res_ph = ""
                    
            team_anova = pd.DataFrame([{'Team': t,
                                        'Metric': metric,
                                        'ANOVA_res': res,
                                        'Post-hoc_res': res_ph}])
    
            tbl_anova = pd.concat([tbl_anova, team_anova], ignore_index=True)
    
    return tbl_anova


def stat_report_anova_period(data):
    order = ['R1', 'R2', 'R3', 'R4', 'R5']
    tbl_anova = pd.DataFrame()
    
    for t in data['Possession'].unique():
        data_t = data[data['Possession'].str.contains(t)].copy()

        for c in data_t['Chrono'].unique():
            data_t_c = data_t[data_t['Chrono']==c].copy()
            for metric in ['Duration', 'Phases', 'Rucks-Passes Ratio', 'Progress +', 'Progress Ratio', 'Zones Progress']:
                anova_groups = []
                shapiro_p = []

                for r in data_t_c['Round'].unique():
                    data_r = data_t_c[data_t_c['Round']==r].copy()
                    if len(data_r) < 3:
                        shapiro_p.append('NA')
                    else:
                        shap_p = round(stats.shapiro(data_r[metric]).pvalue, 3)
                        shapiro_p.append(shap_p)
                        anova_groups.append(data_r[metric])

                if not 'NA' in shapiro_p:
                    lev_p = round(stats.levene(*anova_groups, center='mean').pvalue, 3)
                    normality_check = [s for s in shapiro_p if s > .05]

                    if len(normality_check) == len(shapiro_p) and lev_p > .05:
                        anova_ = stats.f_oneway(*anova_groups)
                        if anova_.pvalue > 0.05:
                            res = f"""An ANOVA test suggests that the difference is not statistically significant between games/periods  
                                    (F={round(anova_.statistic, 2)}, p={round(anova_.pvalue, 2)})."""
                            res_ph = ""
                        else:
                            res = f"""An ANOVA test suggests that the difference is statistically significant for at least one game/period
                                    (F={round(anova_.statistic, 2)}, p={round(anova_.pvalue, 2)}*)."""
                            #Post-hoc
                            post_hoc_matrix = sp.posthoc_tukey(data_t_c, val_col=metric, group_col='Round')
                            post_hoc_matrix = post_hoc_matrix[order].reindex(order)

                            posthoc_res = pd.DataFrame(post_hoc_matrix.stack())
                            posthoc_res = posthoc_res.rename(columns={0: 'Tukey (p-value)'})
                            posthoc_res = round(posthoc_res, 3)
                            posthoc_res = posthoc_res[posthoc_res['Tukey (p-value)']<.05].copy()

                            for idx in posthoc_res.index:
                                posthoc_res.loc[idx, "Cohen's d"] = cohen_d(data_t_c[metric][data_t_c['Round']==idx[0]],
                                                                             data_t_c[metric][data_t_c['Round']==idx[1]])
                            
                            posthoc_res['d abs.'] = np.abs(posthoc_res["Cohen's d"])
                            posthoc_res = posthoc_res.drop_duplicates(subset='d abs.')

                            posthoc_res['Tukey (p-value)'] = ['< 0.05*' if p==0 else f'{p}*' if p<.05 else str(p) for p in posthoc_res['Tukey (p-value)']]
                            posthoc_res["Cohen's d"] = round(posthoc_res["Cohen's d"], 2)
                            posthoc_res = posthoc_res.drop(columns='d abs.')

                            if posthoc_res.empty:
                                res_ph = "The post-hoc test ultimately did not find a statistically significant difference."
                            else:
                                res_ph = posthoc_res.to_json()
                    else:
                        kruskal_ = stats.kruskal(*anova_groups)
                        if kruskal_.pvalue < 0.05:
                            res = f"""A Kruskal-Wallis test suggests that the difference is statistically significant for at least one game/period
                                    (F={round(kruskal_.statistic, 2)}, p={round(kruskal_.pvalue, 2)}*)."""
                            #Post-hoc
                            post_hoc_matrix = sp.posthoc_conover(data_t_c, val_col=metric, group_col='Round')
                            post_hoc_matrix = post_hoc_matrix[order].reindex(order)

                            posthoc_res = pd.DataFrame(post_hoc_matrix.stack())
                            posthoc_res = posthoc_res.rename(columns={0: 'Conover (p-value)'})
                            posthoc_res = round(posthoc_res, 3)
                            posthoc_res = posthoc_res[posthoc_res['Conover (p-value)']<.05].copy()
                            
                            for idx in posthoc_res.index:
                                posthoc_res.loc[idx, "Cohen's d"] = cohen_d(data_t_c[metric][data_t_c['Round']==idx[0]],
                                                                             data_t_c[metric][data_t_c['Round']==idx[1]])
                                
                            posthoc_res['d abs.'] = np.abs(posthoc_res["Cohen's d"])
                            posthoc_res = posthoc_res.drop_duplicates(subset='d abs.')

                            posthoc_res['Conover (p-value)'] = ['< 0.05*' if p==0 else f'{p}*' if p<.05 else str(p) for p in posthoc_res['Conover (p-value)']]
                            posthoc_res["Cohen's d"] = round(posthoc_res["Cohen's d"], 2)
                            posthoc_res = posthoc_res.drop(columns='d abs.')

                            if posthoc_res.empty:
                                res_ph = "The post-hoc test ultimately did not find a statistically significant difference."
                            else:
                                res_ph = posthoc_res.to_json()
                        else:
                            res = f"""A Kruskal-Wallis test suggests that the difference is not statistically significant between games/periods 
                                    (H={round(kruskal_.statistic, 2)}, p={round(kruskal_.pvalue, 2)})."""
                            res_ph = ""
                else:
                    res = "The number of data points from a game is short for testing"
                    res_ph = ''
                    
                team_anova = pd.DataFrame([{'Team': t,
                                            'Chrono': c,
                                            'Metric': metric,
                                            'ANOVA_res': res,
                                            'Post-hoc_res': res_ph}])
        
                tbl_anova = pd.concat([tbl_anova, team_anova], ignore_index=True)
    
    return tbl_anova