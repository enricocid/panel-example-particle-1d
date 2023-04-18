import numpy as np
import panel as pn
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pn.extension('plotly')


""" 
see: 
https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Supplemental_Modules_(Physical_and_Theoretical_Chemistry)/Quantum_Mechanics/05.5%3A_Particle_in_Boxes/Particle_in_a_1-Dimensional_box
 """
def psi(n, L, x):
    A = np.sqrt(2/L)
    return A*np.sin(n*np.pi*x/L)
  

def solve_f(n, L, x, sample_size):
    # solve f(x) for n
    f = np.zeros(sample_size)
    for i in range(sample_size):
        f[i] = psi(n, L , x[i])
    return f


def create_plots():
    
    slider = pn.widgets.IntSlider(name='n', start=1, end=10)

    s_slider = pn.widgets.IntSlider(name='Sample size', start=100, end=150)
    
    @pn.depends(slider.param.value, s_slider.param.value)
    def solve_psi_plot(n, sample_size):

        L = 1

        x = np.linspace(0, L, sample_size)

        f = solve_f(n, L, x, sample_size)

        fig = make_subplots(rows=1, cols=2)

        fig.add_trace(
            go.Scatter(x=x, y=f, name=f'psi', mode ='lines'),
            row=1, col=1
            )

        fig.add_trace(
            go.Scatter(x=x, y = f**2, name=f'psi^2', mode ='lines'),
            row=1, col=2
            )
  
        fig.layout.autosize = True
        return pn.pane.Plotly(fig, config={'responsive':True}, sizing_mode='stretch_width')

    return pn.Column(pn.Row(slider, s_slider), solve_psi_plot)


def create_dashboard():
    """ This function creates the main dashboard """

    reg_selector = create_plots()

    # Inizialize the FastListTemplate
    template = pn.template.FastListTemplate(title='Particle in 1-D infinite box',
                                            main=[reg_selector])
    return template


if __name__.startswith('bokeh'):

    # Create the dashboard and turn into a deployable application
    dashboard = create_dashboard()
    dashboad.servable()
