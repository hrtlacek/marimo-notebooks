# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "lcapy==1.26",
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
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.signal as sig
    from wigglystuff import ChartPuck
    N = 100
    π = np.pi
    return ChartPuck, N, np, plt, π


@app.cell
def _(irplot, mo, widget):
    mo.hstack([widget, irplot], gap=0., justify="start", align="center")

    return


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
    ax.set_title("Drag the puck to change pole!")
    ax.grid(True, alpha=0.3)
    puck = ChartPuck(fig, x=0, y=0)
    plt.close(fig)

    widget = mo.ui.anywidget(puck)


    return (widget,)


@app.cell
def _(N, mo, np, plt, widget, π):
    p = widget.x[0] + 1j*widget.y[0]
    ω = np.linspace(0, π, N)
    z = np.exp(1j*ω)
    H = lambda z: 1 / (1 -p*z**-1)
    figtf, axtf = plt.subplots(1,2,figsize=(8, 3))
    axtf[0].plot(ω,20*np.log10(abs(H(z)+1e-6)))
    axtf[0].set_ylim([-6,30])
    mag = mo.ui.matplotlib(axtf[0])

    h = np.fft.irfft(H(z),N*2)
    h = np.fft.fftshift(h)
    ns = np.arange(N*2)-N
    axtf[1].plot(ns, h)
    axtf[1].set_title("Impulse Response, $h[n]$")
    axtf[1].set_xlabel('$n$')
    plt.grid(True,alpha=0.3)
    plt.ylim([-1,1])
    irplot = mo.ui.matplotlib(axtf[1])
    return (irplot,)


@app.cell
def _():

    # p
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
