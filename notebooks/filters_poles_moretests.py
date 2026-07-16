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
def _(mo):
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    import base64, io
    from wigglystuff import ChartPuck
    style_path = str(mo.notebook_location() / "public" / "matplotlibrc")
    plt.style.use(style_path)
    sr = 44100
    N = 200
    π = np.pi
    return ChartPuck, N, base64, io, np, plt, sr, wavfile, π


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Markdown Test
    $$ H(z) = \frac{1}{1-p\cdot z^{-1}}$$
    """)
    return


@app.cell
def _(base64, h, io, irplot, mo, np, sr, wavfile, widget):
    buf = io.BytesIO()
    wavfile.write(buf, rate=sr, data=h.astype(np.float32))  # your_array: int16 or float32
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    aud = mo.Html(f'<audio controls src="data:audio/wav;base64,{b64}"></audio>')

    mo.vstack([mo.hstack([widget, irplot], gap=0., justify="start", align="center"), aud])
    return


@app.cell
def _(ChartPuck, N, mo, np, π):
    def draw_fn(ax, widget):
        fig = ax.figure

        if not hasattr(fig, "_extra_axes"):
            ax.set_position([0.05, 0.15, 0.28, 0.75])
            ax_topL = fig.add_axes([0.40, 0.55, 0.25, 0.35])
            ax_botL = fig.add_axes([0.40, 0.15, 0.25, 0.35])
            ax_right = fig.add_axes([0.70, 0.15, 0.25, 0.75])
            fig._extra_axes = (ax_topL, ax_botL, ax_right)

        ax_topL, ax_botL, ax_right = fig._extra_axes
        ax.clear(); ax_topL.clear(); ax_botL.clear(); ax_right.clear()

        p = widget.x[0] + 1j * widget.y[0]

        # ---- pole-zero plot (on the puck's own ax) ----
        θ_uc = np.linspace(0, 2*π, 100)
        uc = np.exp(1j*θ_uc)
        ax.plot(np.real(uc), np.imag(uc), alpha=0.6)
        ax.plot(p.real, p.imag, "x", color="red", markersize=10)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1)
        ax.axhline(); ax.axvline()
        ax.set_title("Drag the pole!")
        ax.grid(True, alpha=0.3)

        ω = np.linspace(0, π, N)
        z = np.exp(1j*ω)
        H = lambda z: 1 / (1 - p*z**-1)

        ax_topL.axvline(np.angle(p), c='r')
        ax_topL.plot(ω, 20*np.log10(abs(H(z)) + 1e-6))
        ax_topL.set_ylim([-6, 30]); ax_topL.set_xlim([0, π])
        ax_topL.set_title("Magnitude $|H(\\omega)|$")

        ax_botL.plot(ω, np.angle(H(z)))
        ax_botL.axvline(np.angle(p), c='r')
        ax_botL.set_title(r"Phase $\angle H(\omega)$")
        ax_botL.set_ylim([-π, π]); ax_botL.set_xlim([0, π])

        h = np.fft.fftshift(np.fft.irfft(H(z), N*2))
        ns = np.arange(N*2) - N
        cut = slice(190, 20 + N)
        ax_right.stem(ns[cut], h[cut])
        ax_right.plot(ns[cut], h[cut], 'r')
        ax_right.set_title("Impulse Response, $h[n]$")
        ax_right.set_ylim([-1.5, 1.5])
        ax_right.grid(True, alpha=0.3)

    puck = ChartPuck.from_callback(
        draw_fn=draw_fn,
        x_bounds=(-1.1, 1.1), y_bounds=(-1.1, 1.1),
        figsize=(9, 3.5),
        x=0, y=0,throttle='dragend'
    )
    widget = mo.ui.anywidget(puck)
    widget
    return (widget,)


@app.cell
def _(np):



    def get2dH(H, N_img = 10):
        rvals = np.linspace(-1,1, N_img)
        ivals = np.linspace(-1,1, N_img)
    
        magImg = np.zeros([N_img, N_img])
    
        for _i in range(N_img):
            for _j in range(N_img):
                _z = rvals[_i] + 1j*ivals[_j]
                magVal = abs(H(_z))
                magImg[_i, _j] = magVal
        return magImg


    # ax.imshow(magImg,extent=[-1,1,-1,1], cmap='jet', vmax=2, interpolation='bicubic')

    # figtf, axtf = plt.subplots(1,2,figsize=(8, 3),tight_layout=True)

    return


@app.cell
def _(plt):

    plt.show()
    return


@app.cell
def _(np):
    np.linspace()
    return


if __name__ == "__main__":
    app.run()
