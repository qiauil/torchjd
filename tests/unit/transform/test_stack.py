import torch
from unit.transform.utils import FakeGradientsTransform, assert_tensor_dicts_are_close

from torchjd.transform import EmptyTensorDict, Stack


def test_stack_single_key():
    """
    Tests that the Stack transform correctly stacks gradients into a jacobian, in a very simple
    example with 2 transforms sharing the same key.
    """

    key = torch.zeros([3, 4])
    input = EmptyTensorDict()

    transform = FakeGradientsTransform([key])
    stack = Stack([transform, transform])

    output = stack(input)
    expected_output = {key: torch.ones([2, 3, 4])}

    assert_tensor_dicts_are_close(output, expected_output)


def test_stack_disjoint_key_sets():
    """
    Tests that the Stack transform correctly stacks gradients into a jacobian, in an example where
    the output key sets of all of its transforms are disjoint. The missing values should be replaced
    by zeros.
    """

    key1 = torch.zeros([1, 2])
    key2 = torch.zeros([3])
    input = EmptyTensorDict()

    transform1 = FakeGradientsTransform([key1])
    transform2 = FakeGradientsTransform([key2])
    stack = Stack([transform1, transform2])

    output = stack(input)
    expected_output = {
        key1: torch.tensor([[[1.0, 1.0]], [[0.0, 0.0]]]),
        key2: torch.tensor([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]),
    }

    assert_tensor_dicts_are_close(output, expected_output)


def test_stack_overlapping_key_sets():
    """
    Tests that the Stack transform correctly stacks gradients into a jacobian, in an example where
    the output key sets all of its transforms are overlapping (non-empty intersection, but not
    equal). The missing values should be replaced by zeros.
    """

    key1 = torch.zeros([1, 2])
    key2 = torch.zeros([3])
    key3 = torch.zeros([4])
    input = EmptyTensorDict()

    transform12 = FakeGradientsTransform([key1, key2])
    transform23 = FakeGradientsTransform([key2, key3])
    stack = Stack([transform12, transform23])

    output = stack(input)
    expected_output = {
        key1: torch.tensor([[[1.0, 1.0]], [[0.0, 0.0]]]),
        key2: torch.tensor([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]),
        key3: torch.tensor([[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0]]),
    }

    assert_tensor_dicts_are_close(output, expected_output)
