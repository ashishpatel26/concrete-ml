"""Tests for the torch to numpy module."""
import inspect
import random
import warnings

import numpy
import pytest
from sklearn import tree
from sklearn.exceptions import ConvergenceWarning

from concrete.ml.pytest.utils import classifiers, regressors, sanitize_test_and_train_datasets


def test_seed_1():
    """Test python and numpy seeding."""

    # Python random
    for _ in range(10):
        print(random.randint(0, 1000))

    # Numpy random
    for _ in range(10):
        print(numpy.random.randint(0, 1000))
        print(numpy.random.uniform(-100, 100, size=(3, 3)))


def test_seed_2():
    """Test python and numpy seeding."""

    # Python random
    for _ in range(20):
        print(random.randint(0, 100))

    # Numpy random
    for _ in range(20):
        print(numpy.random.randint(0, 100))
        print(numpy.random.uniform(-10, 100, size=(3, 3)))


@pytest.mark.parametrize("random_inputs_1", [numpy.random.randint(0, 2**15, size=20)])
@pytest.mark.parametrize("random_inputs_2", [numpy.random.randint(-1000, 2**15, size=20)])
@pytest.mark.parametrize("random_inputs_3", [numpy.random.randint(-100, 2**15, size=20)])
def test_seed_needing_randomly_seed_arg_1(random_inputs_1, random_inputs_2, random_inputs_3):
    """Test python and numpy seeding for pytest parameters.

    Remark this test needs an extra --randomly-seed argument for reproducibility
    """

    print("Random inputs", random_inputs_1)
    print("Random inputs", random_inputs_2)
    print("Random inputs", random_inputs_3)


@pytest.mark.parametrize("random_inputs_1", [numpy.random.uniform(0, 2**15, size=20)])
@pytest.mark.parametrize("random_inputs_2", [numpy.random.uniform(-1000, 2**15, size=20)])
@pytest.mark.parametrize("random_inputs_3", [numpy.random.uniform(-100, 2**15, size=20)])
def test_seed_needing_randomly_seed_arg_2(random_inputs_1, random_inputs_2, random_inputs_3):
    """Test python and numpy seeding for pytest parameters.

    Remark this test needs an extra --randomly-seed argument for reproducibility
    """

    print("Random inputs", random_inputs_1)
    print("Random inputs", random_inputs_2)
    print("Random inputs", random_inputs_3)


@pytest.mark.parametrize("random_inputs_1", [numpy.random.randint(0, 2**15, size=20)])
@pytest.mark.parametrize("random_inputs_2", [numpy.random.uniform(-1000, 2**15, size=20)])
@pytest.mark.parametrize("random_inputs_3", [numpy.random.randint(-100, 2**15, size=20)])
def test_seed_needing_randomly_seed_arg_3(random_inputs_1, random_inputs_2, random_inputs_3):
    """Test python and numpy seeding for pytest parameters.

    Remark this test needs an extra --randomly-seed argument for reproducibility
    """

    print("Random inputs", random_inputs_1)
    print("Random inputs", random_inputs_2)
    print("Random inputs", random_inputs_3)


@pytest.mark.parametrize("model, parameters", classifiers + regressors)
def test_seed_sklearn(model, parameters, load_data, default_configuration):
    """Test seeding of sklearn models"""

    x, y = load_data(**parameters)
    model_params, x, _, x_train, y_train, _ = sanitize_test_and_train_datasets(model, x, y)

    # Force "random_state": if it was there, it is overwritten; if it was not there, it is added
    if "random_state" in inspect.getfullargspec(model).args:
        model_params["random_state"] = numpy.random.randint(0, 2**15)
    model = model(**model_params)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ConvergenceWarning)
        # Fit the model
        model, sklearn_model = model.fit_benchmark(x_train, y_train)

    lpvoid_ptr_plot_tree = getattr(model, "plot_tree", None)
    if callable(lpvoid_ptr_plot_tree):
        print("model", tree.plot_tree(model.sklearn_model))

    print("model", sklearn_model)

    # Test the determinism of our package (even if the bitwidth may be too large)
    try:
        model.compile(x, configuration=default_configuration, show_mlir=True)
    except RuntimeError as err:
        print(err)
    except AssertionError as err:
        print(err)
