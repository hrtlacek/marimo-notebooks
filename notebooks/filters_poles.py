# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.14",
#     "matplotlib==3.11.0",
#     "numpy==2.5.1",
#     "scipy==1.18.0",
#     "wigglystuff==0.5.13",
# ]
# ///

import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo, tf_wi, widget):

    mo.hstack([widget, tf_wi])

    return


@app.cell
def _():

    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.signal as sig
    from wigglystuff import ChartPuck
    sr = 44100
    T = 20
    N = int(T*sr)
    t = np.arange(N)/sr
    π = np.pi
    return ChartPuck, np, plt, π


@app.cell
def _(ChartPuck, mo, np, plt, π):
    fig, ax = plt.subplots(figsize=(3, 3))
    ω_uc = np.linspace(0, 2*π,100)
    uc = np.exp(1j*ω_uc)
    ax.plot(np.real(uc), np.imag(uc), alpha=0.6)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axhline()
    ax.axvline()
    ax.set_title("Drag the puck to select coordinates")
    ax.grid(True, alpha=0.3)
    puck = ChartPuck(fig, x=0, y=0)
    plt.close(fig)

    widget = mo.ui.anywidget(puck)


    return (widget,)


@app.cell
def _(mo, np, plt, widget, π):


    # ax = gca()
    p = widget.x[0] + 1j*widget.y[0]
    ω = np.linspace(0, π, 100)
    z = np.exp(1j*ω)
    H = lambda z: 1 / (1 -p*z**-1)
    figtf, axtf = plt.subplots(figsize=(3, 3))
    axtf.plot(abs(H(z)))
    tf_wi = mo.ui.matplotlib(axtf)
    return p, tf_wi


@app.cell
def _(p):

    p
    return


@app.cell
def _(widget):
    widget.x[0]
    return


@app.cell
def _(widget):
    widget
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
