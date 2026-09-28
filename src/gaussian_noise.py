"""
Add white Gaussian noise to a signal, specifying the noise level by ONE of:

    snr_db          -> SNR in dB
    snr             -> SNR as a linear power ratio (Psignal / Pnoise)
    noise_power_db  -> noise power in dB (10*log10 of power, same units as signal^2)
    noise_power     -> noise power, linear (= variance of the noise)
    noise_std       -> noise amplitude as standard deviation (= RMS amplitude)

Works with real and complex signals. For complex signals the noise power is
split equally between the real and imaginary parts.
"""
import numpy as np


def signal_power(x):
    """Average power of a signal: mean(|x|^2)."""
    x = np.asarray(x)
    return np.mean(np.abs(x) ** 2)


def add_gaussian_noise(
    x,
    snr_db=None,
    snr=None,
    noise_power_db=None,
    noise_power=None,
    noise_std=None,
    rng=None,
    return_noise=False,
):
    """
    Add zero-mean white Gaussian noise to `x`.

    Exactly one of the noise-level parameters must be given.

    Parameters
    ----------
    x : array_like (real or complex)
    snr_db : float           SNR in dB, measured against the power of `x`.
    snr : float              SNR as linear power ratio (Ps / Pn).
    noise_power_db : float   Noise power in dB (10*log10(Pn)).
    noise_power : float      Noise power, linear (variance).
    noise_std : float        Noise standard deviation (RMS amplitude).
    rng : int | np.random.Generator | None
         Seed or generator for reproducibility.
    return_noise : bool      Also return the noise array.

    Returns
    -------
    y (and noise, if return_noise=True)
    """
    x = np.asarray(x)

    given = [p is not None for p in
             (snr_db, snr, noise_power_db, noise_power, noise_std)]
    if sum(given) != 1:
        raise ValueError("Specify exactly one of: snr_db, snr, "
                         "noise_power_db, noise_power, noise_std.")

    # Resolve everything to a linear noise power (variance)
    if snr_db is not None:
        pn = signal_power(x) / 10 ** (snr_db / 10)
    elif snr is not None:
        if snr <= 0:
            raise ValueError("Linear SNR must be > 0.")
        pn = signal_power(x) / snr
    elif noise_power_db is not None:
        pn = 10 ** (noise_power_db / 10)
    elif noise_power is not None:
        pn = noise_power
    else:
        pn = noise_std ** 2

    if pn < 0:
        raise ValueError("Noise power cannot be negative.")

    rng = rng if isinstance(rng, np.random.Generator) else np.random.default_rng(rng)

    if np.iscomplexobj(x):
        s = np.sqrt(pn / 2)
        noise = s * (rng.standard_normal(x.shape) + 1j * rng.standard_normal(x.shape))
    else:
        noise = np.sqrt(pn) * rng.standard_normal(x.shape)

    y = x + noise
    return (y, noise) if return_noise else y


def measured_snr_db(signal, noise):
    """Empirical SNR in dB between a clean signal and a noise array."""
    return 10 * np.log10(signal_power(signal) / signal_power(noise))


if __name__ == "__main__":
    t = np.linspace(0, 1, 100_000, endpoint=False)
    x = np.sin(2 * np.pi * 50 * t)              # signal power = 0.5

    # 1) SNR in dB
    y, n = add_gaussian_noise(x, snr_db=10, rng=0, return_noise=True)
    print(f"snr_db=10           -> measured {measured_snr_db(x, n):.2f} dB")

    # 2) SNR linear (10 dB == 10x)
    y, n = add_gaussian_noise(x, snr=10, rng=0, return_noise=True)
    print(f"snr=10 (linear)     -> measured {measured_snr_db(x, n):.2f} dB")

    # 3) Noise power in dB (-20 dB -> 0.01)
    y, n = add_gaussian_noise(x, noise_power_db=-20, rng=0, return_noise=True)
    print(f"noise_power_db=-20  -> power {signal_power(n):.4f} (expected 0.01)")

    # 4) Noise power linear
    y, n = add_gaussian_noise(x, noise_power=0.01, rng=0, return_noise=True)
    print(f"noise_power=0.01    -> power {signal_power(n):.4f}")

    # 5) Amplitude (std)
    y, n = add_gaussian_noise(x, noise_std=0.1, rng=0, return_noise=True)
    print(f"noise_std=0.1       -> std {n.std():.4f}")

    # 6) Complex signal
    xc = np.exp(2j * np.pi * 50 * t)            # power = 1
    y, n = add_gaussian_noise(xc, snr_db=15, rng=0, return_noise=True)
    print(f"complex, snr_db=15  -> measured {measured_snr_db(xc, n):.2f} dB")
