
from plotly import graph_objs as go
import plotly.io as pio
from plotly.offline import iplot, init_notebook_mode
import textwrap

init_notebook_mode(connected=True)


def funnel_plot(funnel_info,figname):
    phases,values = zip(*sorted(list(funnel_info.items()),key=lambda x: x[1],reverse=True))
    
    black = 'rgb(0,0,0)'
    white = 'rgb(255,255,255)'
    grey = 'rgb(180,150,160)'
    
    # Create shapes
    n_phase = len(phases)
    plot_width = 400

    # height of a section and difference between sections 
    section_h = 30
    section_d = 2

    # multiplication factor to calculate the width of other sections
    unit_width = plot_width / max(values)

    # width of each funnel section relative to the plot width
    phase_w = [int(value * unit_width) for value in values]

    # plot height based on the number of sections and the gap in between them
    height = section_h * n_phase + section_d * (n_phase - 1)
    shapes = []
    label_y = [] # list containing the Y-axis location for each section's name and value text
    phase_labels = [] #list containing the wrapped phase label
    for i in range(n_phase):
        if (i == n_phase-1):
                points = [phase_w[i] / 2, height, phase_w[i] / 2, height - section_h]
        else:
                points = [phase_w[i] / 2, height, phase_w[i+1] / 2, height - section_h]

        path = 'M {0} {1} L {2} {3} L -{2} {3} L -{0} {1} Z'.format(*points)

        shape = {
                'type': 'path',
                'path': path,
                'opacity':0.3,
                'fillcolor': grey,
                'line': {
                    'width': 1,
                    'color': white,
                }
        }
        shapes.append(shape)

        # Y-axis location for this section's details (text)
        label_y.append(height - (section_h / 2)) 

        height = height - (section_h + section_d)
        
        fontwidth=5 #todo: make this less stupid (make a function that measures pixel length of string) 
        phase_labels.append(textwrap.fill(phases[i],int(phase_w[i]/fontwidth)))
    
    # For phase names
    label_trace = go.Scatter(
#         x=[-350]*n_phase,
        x=[0]*n_phase,
        y=label_y,
        mode='text',
        text=phase_labels,
        textfont=dict(
            color=black,
            size=15
        )
    )

    # For phase values
    value_trace = go.Scatter(
        x=[200]*n_phase,
        y=label_y,
        mode='text',
        text=values,
        textfont=dict(
            color=black,
            size=15
        )
    )

    data = [label_trace, value_trace]

    layout = go.Layout(
        shapes=shapes,
        height=560,
        width=800,
        showlegend=False,
        xaxis=dict(
            showticklabels=False,
            zeroline=False,
            showgrid=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        )
    )

    fig = go.Figure(data=data, layout=layout)
    pio.write_image(fig, '../figures/'+figname)
    return fig
