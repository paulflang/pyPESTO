from typing import Dict
from .parallel_tempering_methods import sample_parallel_tempering

def parallel_tempering(
        settings: Dict) -> Dict:
    '''

    Parameters
    ----------
    settings

    Returns
    -------

    '''
    # Initialize sampling history
    samplers = [settings['sampler'](settings=settings) for n_T in range(settings['n_temperatures'])]

    # Perform parallel tempering
    result = sample_parallel_tempering(samplers,
                                       settings)
    return result