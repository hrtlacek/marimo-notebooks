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
def _(base64, colorplot, h, io, irplot, mo, np, sr, wavfile, widget):
    buf = io.BytesIO()
    wavfile.write(buf, rate=sr, data=h.astype(np.float32))  # your_array: int16 or float32
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    aud = mo.Html(f'<audio controls src="data:audio/wav;base64,{b64}"></audio>')

    mo.vstack([mo.hstack([widget, irplot], gap=0., justify="start", align="center"), aud, colorplot])
    return


@app.cell
def _(ChartPuck, mo, np, plt, π):
    fig, ax = plt.subplots(figsize=(3, 3), tight_layout=True)
    ω_uc = np.linspace(0, 2*π,100)
    uc = np.exp(1j*ω_uc)
    ax.plot(np.real(uc), np.imag(uc), alpha=0.6)




    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel("real")
    ax.set_ylabel("imaginary")
    ax.axhline()
    ax.axvline()
    ax.set_title("Drag the pole!")
    ax.grid(True, alpha=0.3)
    puck = ChartPuck(fig, x=0.9, y=0, puck_radius=5, throttle=30)
    plt.close(fig)

    widget = mo.ui.anywidget(puck)



    # def draw_fn(axes, widget):
        # ax.clear()
        # draw whatever depends on widget.x / widget.y here


    # puck = ChartPuck.from_callback(
    #     draw_fn=draw_fn,
    #     x_bounds=(-1.5, 1.5),
    #     y_bounds=(-1.5, 1.5),
    #     figsize=(3, 3),
    #     x=0, y=0,
    # )
    # widget = mo.ui.anywidget(puck)


    # plt.
    return (widget,)


@app.cell
def _(N, mo, np, plt, widget, π):



    p = widget.x[0] + 1j*widget.y[0]
    ω = np.linspace(0, π, N)
    z = np.exp(1j*ω)
    H = lambda z: 1 / (1 -p*z**-1)

    N_img = 10
    rvals = np.linspace(-1.1,1.1, N_img)
    ivals = np.linspace(-1.1,1.1, N_img)

    magImg = np.zeros([N_img, N_img])

    for _i in range(N_img):
        for _j in range(N_img):
            _z = rvals[_j] + 1j*ivals[_i]
            magVal = abs(H(_z))
            magImg[_i, _j] = magVal
    figCol, axCol = plt.subplots(1,1,figsize=(8, 3),tight_layout=True)
    axCol.imshow(magImg,extent=[-1.1,1.1,-1.1,1.1], cmap='jet', vmax=2, interpolation='bicubic', origin='lower')
    axCol.scatter(np.real(p), np.imag(p), marker='x')

    colorplot = mo.ui.matplotlib(axCol)


    figtf, axd = plt.subplot_mosaic(
        [
            ["topL", "right"],
            ["bottomL", "right"],
        ],
        figsize=(8, 3),tight_layout=True
    )


    # ------Magnitude
    axd['topL'].plot(ω,20*np.log10(abs(H(z)+1e-6)))
    axd['topL'].set_ylim([-6,30])
    axd['topL'].set_xlim([0,π])
    axd['topL'].set_title("Magnitude $|H(\omega)|$")
    axd['topL'].set_ylabel('$dB$')
    axd['topL'].axvline(np.angle(p), c='r')
    axd['topL'].axhline(0, c='w', ls='--')

    # --------Phase
    axd['bottomL'].plot(ω,np.angle((H(z))))
    axd['bottomL'].set_title(r"Phase $\angle H(\omega)$")
    axd['bottomL'].set_xlabel('$\omega$')
    axd['bottomL'].axvline(np.angle(p), c='r')
    axd['bottomL'].set_ylim([-π,π])
    axd['bottomL'].set_xlim([0,π])
    axd['bottomL'].axhline(0, c='w', ls='--')

    # ----------IR
    cutIR_start = 190
    cutIR_end = 20+N
    h = np.fft.irfft(H(z),N*2)
    h = np.fft.fftshift(h)
    ns = np.arange(N*2)-N
    axd['right'].stem(ns[cutIR_start:cutIR_end], h[cutIR_start:cutIR_end])
    axd['right'].plot(ns[cutIR_start:cutIR_end], h[cutIR_start:cutIR_end], 'r')
    axd['right'].set_title("Impulse Response, $h[n]$")
    axd['right'].set_xlabel('$n$')
    axd['right'].grid(True,alpha=0.3)
    axd['right'].set_ylim([-1.5,1.5])
    irplot = mo.ui.matplotlib(axd['right'])
    return colorplot, h, irplot


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
