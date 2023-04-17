"""
Runs all the notebook referenced in a _toc.yml file
"""
import os
import sys

import yaml
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def flatten_yaml(data):
    """
    Yield elements from a nested YAML structure
    """
    if isinstance(data, list):
        for value in data:
            yield from flatten_yaml(value)
    elif isinstance(data, dict):
        for key, value in data.items():
            yield key
            yield from flatten_yaml(value)
    else:
        yield data


def get_notebooks(filename):
    """
    Returns a list of notebooks referenced in a _toc.yml file
    """
    with open(filename) as f:
        toc = yaml.safe_load(f)
    notebooks = []
    for element in flatten_yaml(toc):
        if isinstance(element, str) and element.endswith('.ipynb'):
            notebooks.append(element)
    return notebooks


def run_notebooks(notebooks):
    """
    Runs all the notebooks in a list
    """
    exec_kws = {'timeout': 14400, 'allow_errors': True}
    # Allow environment to override stored kernel name
    if "NB_KERNEL" in os.environ:
        exec_kws["kernel_name"] = os.environ["NB_KERNEL"]
    ep = ExecutePreprocessor(**exec_kws)
    for nb_path in notebooks:
        nb_path = 'book/' + nb_path
        if not os.path.exists(nb_path):
            print(f"Skipping {nb_path} (not found)")
            continue
        print(f"Running {nb_path}")
        with open(nb_path) as f:
            nb = nbformat.read(f, nbformat.NO_CONVERT)
            ep.preprocess(nb, {})
            with open(nb_path, 'w') as f:
                nbformat.write(nb, f)


if __name__ == "__main__":
    fname = sys.argv[1]
    notebooks = get_notebooks(fname)
    run_notebooks(notebooks)
