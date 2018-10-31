import mne
import numpy as np
from scipy.signal import hilbert


def make_epochs(z_hat, info, t_lim, n_times_atom=1):
    """Make Epochs on the activations of atoms.
    n_splits, n_atoms, n_times_valid = z_hat.shape
    n_trials, n_atoms, n_times_epoch = z_hat_epoch.shape
    """
    n_splits, n_atoms, n_times_valid = z_hat.shape
    n_times = n_times_valid + n_times_atom - 1
    # pad with zeros
    padding = np.zeros((n_splits, n_atoms, n_times_atom - 1))
    z_hat = np.concatenate([z_hat, padding], axis=2)
    # reshape into an unique time-serie per atom
    z_hat = np.reshape(z_hat.swapaxes(0, 1), (n_atoms, n_splits * n_times))

    # create trials around the events, using mne
    new_info = mne.create_info(ch_names=n_atoms, sfreq=info['sfreq'])
    rawarray = mne.io.RawArray(data=z_hat, info=new_info, verbose=False)
    t_min, t_max = t_lim
    epochs = mne.Epochs(rawarray, info['events'], info['event_id'],
                        t_min, t_max, verbose=False)
    z_hat_epoched = epochs.get_data()
    return z_hat_epoched


def fast_hilbert(array):
    n_points = array.shape[0]
    n_fft = next_power2(n_points)
    return hilbert(array, n_fft)[:n_points]


def next_power2(num):
    """Compute the smallest power of 2 >= to num.(float -> int)"""
    return 2 ** int(np.ceil(np.log2(num)))
