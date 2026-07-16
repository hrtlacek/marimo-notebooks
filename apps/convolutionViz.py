# /// script
# dependencies = [
#     "marimo",
#     "matplotlib==3.11.0",
#     "numpy==2.5.1",
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
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    return np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Discrete Convolution

    This little app tries to demonstrate one way of visualizing what hapens in digital convolution.
    Our input shall be called $x[n]$, our outpuy $y[n]$ and our convolution kernel/impulse response $h[n]$. Of course $x$ and $h$ can be interchanged as $x*h=g*x$ but in this case we will think about it as described.

    Often, in literature, we see the following formula of obtaining our result $y[n]$:

    $$ y[n] = \sum_{m=0}^{M-1} x[m]\cdot h[n-m]$$

    All kinds of intuitions are tried to build on top of it.

    This little app explores rewriting this on base of commutativity:

    $$ y[n] = \sum_{m=0}^{M-1} x[n-m]\cdot h[m]$$

    The same thing, just $h$ and $x$ exachenged. Now, what does this say?
    $x[n-m]$ can be recognized as our input delayed by $m$ samples. Multiplying it by the $m$th position seems logical: the further the $x$ values lies in the past (the higher $m$) the 'further' we have to look into the impulse response to find the factor to multiply with.

    Or in other words: Every $y[n]$ is a sum of 'reverb tails'. The following visualisaztion illustrates this. All contributing 'reverb tails' are always drawn. Their sum at position $n$ is $y[n]$.
    """)
    return


@app.cell
def _(np):
    N = 10
    M = 4

    x = np.zeros(N)
    x[0] = 1
    x[1] = -0.5
    x[5] = 0.7
    x[6] = 0.7
    x[7] = -0.2

    h = np.zeros(M)
    h[0] = 1
    h[1] = 0.5
    h[2] = 0.3
    h[3] = 0.1
    # h[2] = 0.3
    # h[2] = 0.5
    # h[3] = 0.3
    return M, N, h, x


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Input Signals, $x[n]$ and $h[n]$
    """)
    return


@app.cell
def _(h, mo, plt, x):
    plt.figure(figsize=[7,2], tight_layout=True)
    plt.subplot(121)
    plt.stem(x)
    plt.xlabel('$n$')
    ax = plt.gca()
    ax.set_title('$x[n]$')
    plt.subplot(122)
    plt.stem(h)
    ax = plt.gca()
    ax.set_title('$h[n]$')
    plt.xlabel('$n$')
    # plt.show()
    ax = plt.gca()
    mo.ui.matplotlib(ax)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Compute $y$
    Play with the slider to calculate $y$ step by step.
    """)
    return


@app.cell(hide_code=True)
def _(N, mo, np):
    nslider = mo.ui.slider(steps = np.arange(N), show_value=True, label='$n$')
    nslider
    return (nslider,)


@app.cell
def _(M, N, h, mo, np, nslider, plt, x):
    lenY = N+M
    y = np.zeros(lenY)
    contribLen = N+M*2
    contribInd = np.arange(contribLen)-M
    ind = np.arange(lenY)

    plt.figure(figsize=[7,4])
    nM = int(nslider.value)+1
    xprep = np.pad(x, [M,M])
    for n in range(nM):
        contrib = np.zeros(contribLen)
        plt.clf()
        for m in range(M):
            # xind = max(0,n-m)
            thisContrib = xprep[n-m+M]*h
            y[n] += thisContrib[m]
            startPos = n-m+M
            endPos = n-m+M*2
            contrib = np.zeros(contribLen)
            contrib[startPos:endPos] = thisContrib
            # print(thisContrib)
            if m==0:
                plt.plot(contribInd, contrib, alpha=0.5, c='w', label='contributing factors')
            else:
                plt.plot(contribInd, contrib, alpha=0.5, c='w')

        plt.stem(np.arange(M)+nM-m-1, xprep[nM:nM+M], markerfmt='wo', 
                 label='$x[n,...,n-M]$')

    markerline, stemlines, baseline = plt.stem(ind, y, label='$y[n]$', linefmt='r--', markerfmt='o')
    markerline.set_markerfacecolor('none')
    plt.ylim([-1,1.2])
    plt.xlim([-M,N+M])
    plt.axvline(nM-1, alpha=0.3,label='$n$', ls='--')
    plt.legend(loc=4)
    plt.xlim([-0.2, N+0.2])
    plt.grid(True, alpha=0.2)
    # plt.show()
    ax1 = plt.gca()
    mo.ui.matplotlib(ax1)
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


@app.cell
def _():
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


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
