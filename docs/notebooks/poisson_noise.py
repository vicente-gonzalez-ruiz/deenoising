"""
Add Poisson (shot) noise to a non-negative signal or image.

Unlike Gaussian noise, Poisson noise is signal dependent: each sample x_i is
treated as an expected intensity and the observed value is a Poisson draw.
To control the noise level you choose how many "counts" (photons, events)
correspond to the signal. Fewer counts -> noisier.

Model:   y = Poisson(lam * x) / lam        (output in the original units)
         E[y] = x,   Var[y_i] = x_i / lam

Specify the noise level with EXACTLY ONE of:

    scale    -> lam, counts per unit of signal (bigger = less noise)
    peak     -> expected counts at the signal maximum (lam = peak / max(x))
    snr_db   -> target SNR in dB (global, see notes below)
    snr      -> target SNR as a linear power ratio

SNR definition used for the snr modes:
    SNR = mean(x^2) / mean(Var[y]) = lam * mean(x^2) / mean(x)
so   lam = SNR * mean(x) / mean(x^2).
This is the *expected* global SNR; per-sample SNR varies with the signal level.
"""
import numpy as np


def signal_power(x):
    """Average power of a signal: mean(|x|^2)."""
    x = np.asarray(x)
    return np.mean(np.abs(x) ** 2)


def add_poisson_noise(
    x,
    scale=None,
    peak=None,
    snr_db=None,
    snr=None,
    normalize=True,
    rng=None,
    return_noise=False,
):
    """
    Apply Poisson noise to `x` (must be real and >= 0).

    Parameters
    ----------
    x : array_like, real, non-negative
    scale : float     Counts per unit signal (lam).
    peak : float      Expected counts at max(x). E.g. peak=30 -> very noisy,
                      peak=1000 -> mild noise.
    snr_db : float    Target global SNR in dB.
    snr : float       Target global SNR, linear power ratio.
    normalize : bool  True (default): return y in the original units
                      (Poisson counts / lam). False: return raw integer counts.
    rng : int | np.random.Generator | None
    return_noise : bool   Also return y - x (only meaningful if normalize=True).

    Returns
    -------
    y (and noise, if return_noise=True)
    """
    x = np.asarray(x, dtype=float)

    if np.iscomplexobj(x):
        raise ValueError("Poisson noise is defined for real signals only.")
    if np.any(x < 0):
        raise ValueError("Signal must be non-negative (shift/rescale it first).")

    given = [p is not None for p in (scale, peak, snr_db, snr)]
    if sum(given) != 1:
        raise ValueError("Specify exactly one of: scale, peak, snr_db, snr.")

    # Resolve to lam (counts per unit signal)
    if scale is not None:
        lam = scale
    elif peak is not None:
        xmax = x.max()
        if xmax <= 0:
            raise ValueError("Signal is all zeros; cannot use `peak`.")
        lam = peak / xmax
    else:
        snr_lin = 10 ** (snr_db / 10) if snr_db is not None else snr
        if snr_lin <= 0:
            raise ValueError("SNR must be > 0.")
        m = x.mean()
        if m <= 0:
            raise ValueError("Signal mean is zero; cannot target an SNR.")
        lam = snr_lin * m / np.mean(x ** 2)

    if lam <= 0:
        raise ValueError("Scale must be > 0.")

    rng = rng if isinstance(rng, np.random.Generator) else np.random.default_rng(rng)
    counts = rng.poisson(lam * x)

    if not normalize:
        return counts

    y = counts / lam
    return (y, y - x) if return_noise else y


def measured_snr_db(signal, noise):
    """Empirical SNR in dB between a clean signal and a noise array."""
    return 10 * np.log10(signal_power(signal) / signal_power(noise))


if __name__ == "__main__":
    t = np.linspace(0, 1, 200_000, endpoint=False)
    x = 1.0 + 0.5 * np.sin(2 * np.pi * 50 * t)   # non-negative, max = 1.5

    # 1) Target SNR in dB
    y, n = add_poisson_noise(x, snr_db=20, rng=0, return_noise=True)
    print(f"snr_db=20        -> measured {measured_snr_db(x, n):.2f} dB")

    # 2) Target SNR, linear (100 == 20 dB)
    y, n = add_poisson_noise(x, snr=100, rng=0, return_noise=True)
    print(f"snr=100 (linear) -> measured {measured_snr_db(x, n):.2f} dB")

    # 3) Peak counts
    y, n = add_poisson_noise(x, peak=100, rng=0, return_noise=True)
    print(f"peak=100         -> measured {measured_snr_db(x, n):.2f} dB, "
          f"mean {y.mean():.3f} (clean {x.mean():.3f})")

    # 4) Scale (counts per unit)
    y, n = add_poisson_noise(x, scale=50, rng=0, return_noise=True)
    print(f"scale=50         -> measured {measured_snr_db(x, n):.2f} dB")

    # 5) Raw counts (integers)
    c = add_poisson_noise(x, peak=100, normalize=False, rng=0)
    print(f"raw counts       -> dtype {c.dtype}, max {c.max()}")
