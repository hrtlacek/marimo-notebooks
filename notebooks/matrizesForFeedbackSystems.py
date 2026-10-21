import marimo

__generated_with = "0.23.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Energy Preserving Mixing Matrices

    This notebook explores common matrices used to mix a number of (audio) channels in an energy preserving way, which is particularly useful in rever or general feedback applications.

    All of them are used to mix a number of sinusoid signals. They are checked for orthogonality and energy preservation. Furthermore, they show rather different behaviors when all resulting channels are summed up again which might be the case in audio applications.
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import scipy
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.signal as sig
    import sympy as sp

    return np, plt, scipy, sp


@app.cell
def _(np):
    sr = 10000 
    T = 1
    N = int(sr*T)
    ns = np.arange(N)
    t = ns/sr

    nChans = 8

    freqs = np.expand_dims(np.linspace(100, 800, nChans),axis=0)
    x = np.sin(t*2*np.pi*freqs.T).T
    return N, nChans, sr, x


@app.cell
def _(N, np, plt, sr, x):
    X = np.fft.fft(np.sum(x, axis=1))
    fax = np.fft.fftfreq(N, d=1/sr)
    X = np.fft.fftshift(X)
    fax = np.fft.fftshift(fax)
    plt.plot(fax,20*np.log10(np.abs(X)))
    plt.xlim([0, sr/2])
    plt.show()

    return (fax,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hadamard Matrix
    """)
    return


@app.cell
def _(nChans, np, scipy):
    m_had = np.sqrt(nChans)
    normFact = np.sqrt(nChans)#1/2**(m_had/2)
    A_Had = (1/normFact)*scipy.linalg.hadamard(8)
    A_Had
    return (A_Had,)


@app.cell
def _(A_Had, x):
    y_had = x@A_Had
    return (y_had,)


@app.cell
def _(fax, np, plt, sr, y_had):
    Y_had = np.fft.fft(y_had, axis=0)
    Y_had = np.fft.fftshift(Y_had)
    plt.plot(fax,20*np.log10(np.abs(Y_had)), alpha=0.2)
    plt.xlim([0, sr/2])
    plt.show()


    return


@app.cell
def _(np, x, y_had):
    E_x = np.sum(np.abs(x)**2)
    E_yhad = np.sum(np.abs(y_had)**2)

    if np.isclose(E_x, E_yhad):
        print("Energy Preserving!")
 
    return (E_x,)


@app.cell
def _(A_Had, np):
    np.linalg.det(A_Had)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sum of all channels
    Contains only first channel.
    """)
    return


@app.cell
def _(N, fax, np, plt, y_had):
    plt.plot(fax[N//2-1:], np.abs(np.fft.rfft(np.sum(y_had,axis=1))))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Householder Matrix
    """)
    return


@app.cell
def _(nChans, np, sp):

    v = np.ones(nChans)
    u = v/ np.linalg.norm(v)
    A_hou_unnorm = np.eye(nChans) - 2*np.outer(v, v.T) #Un-normalized form for pretty display
    A_hou = np.eye(nChans) - 2*np.outer(u, u.T) #Normalized to be energy preserving.

    sp.Matrix(A_hou_unnorm)
    return (A_hou,)


@app.cell
def _(A_hou, sp):
    sp.Matrix(A_hou)
    return


@app.cell
def _(A_hou, x):
    y_hou = x@A_hou
    return (y_hou,)


@app.cell
def _(fax, np, plt, sr, y_hou):
    Y_hou = np.fft.fft(y_hou, axis=0)
    Y_hou = np.fft.fftshift(Y_hou)
    plt.plot(fax,20*np.log10(np.abs(Y_hou)), alpha=0.2)
    plt.xlim([0, sr/2])
    plt.show()


    return


@app.cell
def _(E_x, np, y_hou):
    E_yhou = np.sum(np.abs(y_hou)**2)

    if np.isclose(E_x, E_yhou):
        print("Energy Preserving!")
 
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sum of all channels
    contains all channels
    """)
    return


@app.cell
def _(N, fax, np, plt, y_hou):
    plt.plot(fax[N//2-1:], np.abs(np.fft.rfft(np.sum(y_hou,axis=1))))
    return


@app.cell
def _(np, scipy):
    B = scipy.stats.ortho_group.rvs(8)
    np.linalg.det(B)
    B
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Conference Matrix
    https://mathonline.wikidot.com/conference-matrices
    """)
    return


@app.cell
def _(nChans):
    q = nChans-1 # should be an odd prime power..

    Z_q = []
    for i in range(q-1):
        Z_q.append(int((i+1)**2 % q))
    Z_q = list(set(Z_q))

    def ξ(x):
        if int(x) ==0:
            return 0
        if int(x) in Z_q:
            return 1
        else:
            return -1

    return q, ξ


@app.cell
def _(np, q, ξ):
    C = np.ones([q+1, q+1])
    C[0,0] = 0
    for a in range(q+1):
        for b in range(q+1):
            if a >=1 and b >= 1:
                C[a,b] = int(ξ(((a-1)-(b-1)) % q))
    return (C,)


@app.cell
def _(C, sp):
    sp.Matrix(C)
    return


@app.cell
def _(C, nChans, np):
    c1 =np.allclose(C@C.T , (nChans -1) * np.eye(nChans))
    c2 = C.all() in [0,-1,1]
    if c1 and c2:
        print('Correct conference Matrix')
    return


@app.cell
def _(C, np, q, x):
    conNorm = 1 / np.sqrt(q)
    y_con = x@(C*conNorm)
    return (y_con,)


@app.cell
def _(E_x, np, y_con):
    E_ycon = np.sum(np.abs(y_con)**2)

    if np.isclose(E_x, E_ycon):
        print("Energy Preserving!")
 
    return


@app.cell
def _(fax, np, plt, sr, y_con):
    Y_con = np.fft.fft(y_con, axis=0)
    Y_con = np.fft.fftshift(Y_con)
    plt.plot(fax,20*np.log10(np.abs(Y_con)), alpha=0.2)
    plt.xlim([0, sr/2])
    plt.show()


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sum of all channels
    1st channel much stronger than others but all present.
    """)
    return


@app.cell
def _(N, fax, np, plt, y_con):
    plt.plot(fax[N//2-1:], np.abs(np.fft.rfft(np.sum(y_con,axis=1))))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Rotation Matrix

    The reference below gives a procedure to constuct a rotation Matrix from 2 orthonormal basis vectors in arbitrary dimensions. Vectors $n_1$ and $n_2$ here are chosen so the first half of elements of $n_1$ are set to $1$ while the second half of $n_2$ are set to $1$. Both of them are normalized afterwards.

    - https://analyticphysics.com/Higher%20Dimensions/Rotations%20in%20Higher%20Dimensions.htm
    - https://www.appletonaudio.com/blog/2023/high-dimension-rotation-matrices/
    <math xmlns="http://www.w3.org/1998/Math/MathML" displaystyle="true">
      <mrow>
        <mo>exp</mo>
        <mo>&#x2061;</mo>
        <mrow>
          <mo>[</mo>
          <mrow>
            <mi>a</mi>
            <mspace width=".2em"></mspace>
            <msub>
              <mi>L</mi>
              <mrow>
                <msub>
                  <mi mathvariant="bold">n</mi>
                  <mn>1</mn>
                </msub>
                <mo>&#x2062;</mo>
                <msub>
                  <mi mathvariant="bold">n</mi>
                  <mn>2</mn>
                </msub>
              </mrow>
            </msub>
          </mrow>
          <mo>]</mo>
        </mrow>
      </mrow>
      <mo>=</mo>
      <mrow>
        <mi>I</mi>
        <mo>+</mo>
        <mrow>
          <mrow>
            <mo>(</mo>
            <mrow>
              <mrow>
                <msub>
                  <mi mathvariant="bold">n</mi>
                  <mn>2</mn>
                </msub>
                <mo>&#x2062;</mo>
                <msubsup>
                  <mi mathvariant="bold">n</mi>
                  <mn>1</mn>
                  <mi mathvariant="normal">T</mi>
                </msubsup>
              </mrow>
              <mo>-</mo>
              <mrow>
                <msub>
                  <mi mathvariant="bold">n</mi>
                  <mn>1</mn>
                </msub>
                <mo>&#x2062;</mo>
                <msubsup>
                  <mi mathvariant="bold">n</mi>
                  <mn>2</mn>
                  <mi mathvariant="normal">T</mi>
                </msubsup>
              </mrow>
            </mrow>
            <mo>)</mo>
          </mrow>
          <mo>&#x2062;</mo>
          <mrow>
            <mo>sin</mo>
            <mo>&#x2061;</mo>
            <mi>a</mi>
          </mrow>
        </mrow>
        <mo>+</mo>
        <mrow>
          <mrow>
            <mo>(</mo>
            <mrow>
              <mrow>
                <msub>
                  <mi mathvariant="bold">n</mi>
                  <mn>1</mn>
                </msub>
                <mo>&#x2062;</mo>
                <msubsup>
                  <mi mathvariant="bold">n</mi>
                  <mn>1</mn>
                  <mi mathvariant="normal">T</mi>
                </msubsup>
              </mrow>
              <mo>+</mo>
              <mrow>
                <msub>
                  <mi mathvariant="bold">n</mi>
                  <mn>2</mn>
                </msub>
                <mo>&#x2062;</mo>
                <msubsup>
                  <mi mathvariant="bold">n</mi>
                  <mn>2</mn>
                  <mi mathvariant="normal">T</mi>
                </msubsup>
              </mrow>
            </mrow>
            <mo>)</mo>
          </mrow>
          <mo>&#x2062;</mo>
          <mrow>
            <mo>(</mo>
            <mrow>
              <mrow>
                <mo>cos</mo>
                <mo>&#x2061;</mo>
                <mi>a</mi>
              </mrow>
              <mo>-</mo>
              <mn>1</mn>
            </mrow>
            <mo>)</mo>
          </mrow>
        </mrow>
      </mrow>
    </math>
    """)
    return


@app.cell
def _(nChans, np):
    # Define hperplane by 2 n-dimensional vectors. Should be orthogonal unit vectors
    n_1 = np.zeros(nChans)
    n_2 = np.zeros(nChans)
    n_1[:nChans//2] = 1 
    n_2[nChans//2:] = 1

    n_1 = n_1 / np.linalg.norm(n_1)
    n_2 = n_2 / np.linalg.norm(n_2)
    return n_1, n_2


@app.cell
def _(n_1):
    n_1
    return


@app.cell
def _(n_2):
    n_2
    return


@app.cell
def _(n_1, n_2, np):
    if np.isclose(0, np.dot(n_1, n_2)):
        print('n_1 and n_2 are Orthogonal')
    return


@app.cell
def _(n_1, n_2):
    n_2@n_1.T
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that in the following, in practical applications, a lot can be precomputed such as the outer products and the arithmetic on the resulting matrices.
    """)
    return


@app.cell
def _(nChans, n_1, n_2, np):
    R = lambda α: np.eye(nChans) + (np.outer(n_2,n_1.T) - np.outer(n_1,n_2.T))*np.sin(α) + (np.outer(n_1,n_1.T) + np.outer(n_2,n_2.T))*(np.cos(α)-1)
    return (R,)


@app.cell
def _(mo):
    α_s = mo.ui.slider(0, 7, 0.01)
    α_s
    return (α_s,)


@app.cell
def _(R, x, α_s):
    R_mat = R(α_s.value)
    y_rot = x@R_mat
    return R_mat, y_rot


@app.cell
def _(R_mat, mo):
    mo.ui.matrix(R_mat)
    return


@app.cell
def _(R_mat, np):
    np.linalg.det(R_mat)
    return


@app.cell
def _(E_x, np, y_rot):
    E_yrot = np.sum(np.abs(y_rot)**2)

    if np.isclose(E_x, E_yrot):
        print("Energy Preserving!")
 
    return


@app.cell
def _(fax, np, plt, sr, y_rot):
    Y_rot = np.fft.fft(y_rot, axis=0)
    Y_rot = np.fft.fftshift(Y_rot)
    plt.plot(fax,20*np.log10(np.abs(Y_rot)), alpha=0.2)
    plt.xlim([0, sr/2])
    plt.show()


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sum of all channels
    Depend on rotation / angle.
    """)
    return


@app.cell
def _(N, fax, np, plt, y_rot):
    plt.plot(fax[N//2-1:], np.abs(np.fft.rfft(np.sum(y_rot,axis=1))))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
