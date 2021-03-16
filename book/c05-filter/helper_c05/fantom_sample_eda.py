from plotly.subplots import make_subplots
import plotly.graph_objects as go
import textwrap
from myst_nb import glue
import pandas as pd


def create_plot_dfs(samples_info):
    # SEX DONUT PLOT:
    sex_donut = samples_info['Sex'].value_counts(dropna=False)

    # TISSUES + SAMPLE TYPE HISTOGRAM:
    # TODO: Add label that it's for top n tissues only
    tissue = 'Characteristics[Tissue]'
    num_tissues = 50
    glue('num_common_tissues', num_tissues, display=False)
    top_n = samples_info[tissue].value_counts()[:num_tissues]
    tissues_samples = samples_info[[tissue, 'Sample Type']].value_counts()
    tissues_samples = tissues_samples.reset_index(['Sample Type'])
    tissues_samples = tissues_samples.rename(columns={0: 'value counts'})
    tissues_samples = tissues_samples.loc[top_n.index]

    # TODO: Move this to fantom_sample clean?
    anatomical_system = samples_info[samples_info[tissue] == 'ANATOMICAL SYSTEM'].shape[0]
    glue('anatomical-system', anatomical_system, display=False)
    blood_samples = samples_info[samples_info[tissue] == 'blood'].shape[0]
    glue('blood-samples', blood_samples, display=False)
    tissues_less_three = sum(samples_info[tissue].value_counts().sort_values() < 3)
    glue('tissues-less-three', tissues_less_three, display=False)

    # AGES
    nan_age_count = samples_info['Age (years)'].value_counts(dropna=False).iloc[0]

    # PROVIDER + COLLABORATION HISTOGRAM:
    # TODO: Add label that it's for top n collaborators only/mention in caption
    num_collaborators = 10
    glue('num_collaborators', num_collaborators, display=False)
    top_n_collaborators = samples_info['Characteristics [Collaboration]'].value_counts()[:num_collaborators]
    collaborators_providers = samples_info[['Characteristics [Collaboration]', 'Characteristics [Provider]']]
    # doing things in different order to tissue + sample type due to many 'NaNs'
    collaborators_providers = collaborators_providers[collaborators_providers['Characteristics [Collaboration]'].isin(list(top_n_collaborators.index.unique()))]
    collaborators_providers['Characteristics [Provider]'] = collaborators_providers['Characteristics [Provider]'].fillna('unknown')
    collaborators_providers = collaborators_providers.value_counts()
    collaborators_providers = collaborators_providers.reset_index(['Characteristics [Provider]'])
    collaborators_providers = collaborators_providers.rename(columns={0: 'value counts'})
    # Group anything from not the top 10 prividers into "misc providers":
    num_providers = 10
    glue('num_providers', num_providers, display=False)
    chosen_providers = collaborators_providers.groupby(['Characteristics [Provider]']).sum().sort_values(by='value counts', ascending=False)[:num_providers].index
    collaborators_providers.loc[~collaborators_providers['Characteristics [Provider]'].isin(list(chosen_providers)),'Characteristics [Provider]'] = 'misc providers'
    collaborators_providers = collaborators_providers.groupby([collaborators_providers.index, 'Characteristics [Provider]']).sum()
    collaborators_providers = collaborators_providers.reset_index(['Characteristics [Provider]'])

    return sex_donut, tissues_samples, nan_age_count, collaborators_providers


def create_plotly_plots(samples_info, sex_donut, tissues_samples, nan_age_count, collaborators_providers):
    # TODO: load nice colour scheme from file

    # initialise subplot:
    chart_types = [
        [{'type': 'domain'},  # domain type for pie charts
         {'type': 'xy'}],
        [{'type': 'xy'},
         {'type': 'xy'}],
    ]
    fig = make_subplots(rows=2, cols=2,
                        column_widths=[0.3, 0.7],
                        specs=chart_types,
                        subplot_titles=(
                        "(a) sex", "(b) collaborators and providers", "(c) age", "(d) tissues and sample types"),
                        horizontal_spacing=0.1,
                        vertical_spacing=0.35,
                        )

    # (a) sex:
    fig.add_trace(
        go.Pie(labels=sex_donut.index, values=sex_donut.values, hole=.5, name='sex', textinfo='label+percent',
               legendgroup='sex'),
        row=1, col=1,
    )

    # (b) collaboration + provider:
    for provider in collaborators_providers['Characteristics [Provider]'].unique():
        data = collaborators_providers[collaborators_providers['Characteristics [Provider]'] == provider]
        x_tidy = [textwrap.fill(x, width=15).replace('\n', '<br>') for x in list(data.index)]

        trace = go.Bar(
            x=x_tidy,
            y=data['value counts'],
            name=provider,
            legendgroup='provider'
        )
        fig.append_trace(trace, 1, 2)
        fig.update_xaxes(tickfont={'size': 8}, title_text="Collaborators", title_standoff=0, row=1, col=2)
        fig.update_yaxes(tickfont={'size': 8}, title_text="Frequency", row=1, col=2, title_standoff=0)

    # (c) age:
    fig.add_trace(go.Histogram(x=samples_info['Age (years)'], name='Age (years)', nbinsx=30, legendgroup='age'), row=2,
                  col=1, )
    fig.add_trace(
        go.Bar(x=[-10], y=[nan_age_count], hoverinfo='name+y+text', text=['NaN'], name='Age (years)', legendgroup='age'),
        row=2, col=1)
    fig.update_xaxes(
        tickvals=[-10] + list(range(0, 100, 20)),
        ticktext=['NaN'] + list(range(0, 100, 20)),
        row=2, col=1,
        tickfont={'size': 8},
        title_text="Age (years)",
        title_standoff=0)
    fig.update_yaxes(tickfont={'size': 8}, title_text="Frequency", row=2, col=1, title_standoff=0)

    # (d) tissue + sample type:
    for sample_type in ['primary cells', 'tissues - donor', 'tissues - pool']:
        data = tissues_samples[tissues_samples['Sample Type'] == sample_type]
        trace = go.Bar(
            x=data.index,
            y=data['value counts'],
            name=sample_type,
            legendgroup='sample type'
        )
        fig.append_trace(trace, 2, 2)
        fig.update_xaxes(tickfont={'size': 8}, row=2, col=2, title_text="Tissues", title_standoff=0)
        fig.update_yaxes(tickfont={'size': 8}, title_text="Frequency", row=2, col=2, title_standoff=0)

    # Save images:
    fig.update_layout(barmode="stack", showlegend=False, template='seaborn', width=800)
    fig_name = 'fantom_eda'
    fig.write_html(f"../images/{fig_name}.html")
    fig.write_image(f"../images/{fig_name}.png")
    return fig


def anat_system_tbl(samples_info, chosen_samples):
    # Create anatomical system table:
    # TODO: Make a class for these label names somewhere
    descr, tissue, category = ['Charateristics [description]', 'Characteristics[Tissue]', 'Characteristics [Category]']
    anatomical_system_samples = \
        samples_info[samples_info[tissue] == 'ANATOMICAL SYSTEM'].iloc[chosen_samples][[descr, tissue, category]]
    glue("anatomical-system-sample-table", anatomical_system_samples, display=False)
    return anatomical_system_samples
