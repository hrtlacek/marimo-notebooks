# /// script
# dependencies = [
#     "marimo",
#     "matplotlib==3.11.0",
#     "numpy==2.5.1",
#     "scipy==1.18.0",
# ]
# requires-python = ">=3.13"
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
    import base64, io
    from scipy.io import wavfile
    style_path = str(mo.notebook_location() / "public" / "matplotlibrc")
    plt.style.use(style_path)
    return base64, io, np, plt, wavfile


@app.cell
def _(np):
    sr = 44100
    T = 1
    π = np.pi
    N = int(T*sr)
    t = np.arange(N)/sr
    return sr, t, π


@app.cell
def _(base64, io, mo, np, plt, sr, t, wavfile, π):
    f = 100
    ω = 2*π*f
    y = np.sin(t*ω)

    fix,ax = plt.subplots()
    ax.plot(t,y)
    p = mo.ui.matplotlib(ax)

    buf = io.BytesIO()
    wavfile.write(buf, rate=sr, data=y.astype(np.float32))  # your_array: int16 or float32
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    aud = mo.Html(f'<audio controls src="data:audio/wav;base64,{b64}"></audio>')

    mo.vstack([p,aud])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
