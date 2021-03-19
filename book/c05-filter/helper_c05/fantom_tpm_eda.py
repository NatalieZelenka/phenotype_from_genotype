import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import seaborn as sns
import logging
from myst_nb import glue


def create_distribution_plot(samples_info, protein_tpm):
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=("(a) box-plots", "(b) dist-plot"),
                        horizontal_spacing=0.1,
                        shared_xaxes=True)

    tissue_col = 'Characteristics[Tissue]'
    num_tissues = 10
    glue('num-tissues-fpd', num_tissues, display=False)
    cmap = sns.color_palette(n_colors=num_tissues + 1).as_hex()

    n_bins = 50
    bins = np.logspace(0, 5.5, n_bins)

    i = 0
    for tissue in samples_info[tissue_col].value_counts()[:num_tissues].index:
        i += 1
        samples = samples_info[samples_info[tissue_col] == tissue].index
        tissue_tpm = protein_tpm[samples].mean(axis=1) + 1
        fig.add_trace(go.Box(x=tissue_tpm, name=tissue, boxpoints=False, legendgroup=tissue, line_color=cmap[i]), row=1,
                      col=1)

        hist, _ = np.histogram(list(tissue_tpm), bins=bins, density=True)
        fig.add_trace(go.Scatter(x=bins, y=hist, name=tissue, mode='lines+markers', legendgroup=tissue,
                                 marker_color=cmap[i], opacity=0.8), row=2, col=1)
    fig.update_traces(marker={'size': 3})
    fig.update_xaxes(type="log", range=[0, 5.5], tickfont={'size': 8}, title_text="mean(TPM + 1) per protein", title_standoff=0.1)
    fig.update_yaxes(tickfont={'size': 8}, title_text="Tissues", row=1, col=1, title_standoff=0)
    fig.update_yaxes(type="log", tickfont={'size': 8}, title_text="Density", row=2, col=1, title_standoff=75)
    fig.update_layout(xaxis_showgrid=False, template='seaborn', width=800, legend_orientation="h",
                      legend={'x': 0.1, 'y': -0.15})

    fig_name = 'tissue_dists'
    fig.write_html(f"../images/{fig_name}.html")
    # TODO: Get png write working.
    # try:
    #     fig.write_image(f"../images/{fig_name}.png")
    # except ValueError:
    #     logging.info('Could not write png image.')

    return fig
