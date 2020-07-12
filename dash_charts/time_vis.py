"""PLANNED: Sample scripts for TimeVis-like horizontal bar chart with annotations.

Goal would be to implement timevis from R in Plotly/Dash (R/TimeVis https://github.com/daattali/timevis)

Online Gantt Demo: https://chart-studio.plot.ly/create/?fid=tmercieca:5#/

"""

# TODO: See the Gantt chart implementation

# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# import plotly.figure_factory as ff
# import plotly.graph_objs as go
#
# # %qtconsole --style vim
#
# # sample data
# StartA = '2009-01-01'
# StartB = '2009-03-05'
# StartC = '2009-02-20'
#
# FinishA = '2009-02-28'
# FinishB = '2009-04-15'
# FinishC = '2009-05-30'
#
# LabelDateA = '2009-01-25'
# LabelDateB = '2009-03-20'
# LabelDateC = '2009-04-01'
#
# df = [dict(Task="Task A", Start=StartA, Finish=FinishA),
#       dict(Task="Task B", Start=StartB, Finish=FinishB),
#       dict(Task="Task C", Start=StartC, Finish=FinishC)]
#
# fig = ff.create_gantt(df)
#
# # add annotations
# annotations = [dict(x=LabelDateA, y=0, text="Task label A", showarrow=False, font=dict(color='white')),
#                dict(x=LabelDateB, y=1, text="Task label B", showarrow=False, font=dict(color='White')),
#                dict(x=LabelDateC, y=2, text="Task label C", showarrow=False, font=dict(color='White'))]
#
# # plot figure
# fig['layout']['annotations'] = annotations
# fig.show()
#
# # ------------------------------------------------------------------------------
#
# df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
#       dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
#       dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Not Started'),
#       dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-17', Resource='Complete'),
#       dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
#       dict(Task="Job-3", Start='2017-04-01', Finish='2017-04-20', Resource='Not Started'),
#       dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
#       dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]
#
# colors = {'Not Started': 'rgb(220, 0, 0)',
#           'Incomplete': (1, 0.9, 0.16),
#           'Complete': 'rgb(0, 255, 100)'}
#
# fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
#                       group_tasks=True)
# fig.show()
