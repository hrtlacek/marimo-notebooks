# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.14",
# ]
# ///
import marimo

__generated_with = "0.23.13"
app = marimo.App(width="columns")


@app.cell(column=0)
def _(mo, puck):
    widget = mo.ui.anywidget(puck)

    widget
    return (widget,)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.signal as sig
    from wigglystuff import ChartPuck
    sr = 44100
    T = 20
    N = int(T*sr)
    t = np.arange(N)/sr
    π = np.pi
    return ChartPuck, mo, np, plt, π


@app.cell
def _(ChartPuck, np, plt, π):
    fig, ax = plt.subplots(figsize=(6, 6))
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
    return (puck,)


@app.cell
def _(p):

    p
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell(column=1)
def _(np, plt, widget, π):
    p = widget.x[0] + 1j*widget.y[0]
    ω = np.linspace(0, π, 100)
    z = np.exp(1j*ω)
    H = lambda z: 1 / (1 -p*z**-1)
    plt.plot(abs(H(z)))
    return (p,)


if __name__ == "__main__":
    app.run()
