# MIT License
#
# Copyright (C) IBM Corporation 2020
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This module implements the adversarial patch attack `AdversarialPatch`. This attack generates an adversarial patch that
can be printed into the physical world with a common printer. The patch can be used to fool image classifiers.

| Paper link: https://arxiv.org/abs/1712.09665
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from art.attacks.attack import EvasionAttack

logger = logging.getLogger(__name__)


class AdversarialPatchTensorFlow(EvasionAttack):
    """
    Implementation of the adversarial patch attack.

    | Paper link: https://arxiv.org/abs/1712.09665
    """
    attack_params = EvasionAttack.attack_params + [
        "target",
        "rotation_max",
        "scale_min",
        "scale_max",
        "learning_rate",
        "max_iter",
        "batch_size",
        "clip_patch",
    ]

    def __init__(
            self,
            classifier,
            target=0,
            rotation_max=22.5,
            scale_min=0.1,
            scale_max=1.0,
            learning_rate=5.0,
            max_iter=500,
            clip_patch=None,
            batch_size=16,
    ):
        """
        Create an instance of the :class:`.AdversarialPatch`.

        :param classifier: A trained classifier.
        :type classifier: :class:`.Classifier`
        :param target: The target label for the created patch.
        :type target: `int`
        :param rotation_max: The maximum rotation applied to random patches. The value is expected to be in the
               range `[0, 180]`.
        :type rotation_max: `float`
        :param scale_min: The minimum scaling applied to random patches. The value should be in the range `[0, 1]`,
               but less than `scale_max`.
        :type scale_min: `float`
        :param scale_max: The maximum scaling applied to random patches. The value should be in the range `[0, 1]`, but
               larger than `scale_min.`
        :type scale_max: `float`
        :param learning_rate: The learning rate of the optimization.
        :type learning_rate: `float`
        :param max_iter: The number of optimization steps.
        :type max_iter: `int`
        :param clip_patch: The minimum and maximum values for each channel
        :type clip_patch: [(float, float), (float, float), (float, float)]
        :param batch_size: The size of the training batch.
        :type batch_size: `int`
        """
        super(AdversarialPatchTensorFlow, self).__init__(classifier=classifier)
        if not isinstance(classifier, ClassifierNeuralNetwork) or not isinstance(classifier, ClassifierGradients):
            raise ClassifierError(self.__class__, [ClassifierNeuralNetwork, ClassifierGradients], classifier)

        kwargs = {
            "target": target,
            "rotation_max": rotation_max,
            "scale_min": scale_min,
            "scale_max": scale_max,
            "learning_rate": learning_rate,
            "max_iter": max_iter,
            "batch_size": batch_size,
            "clip_patch": clip_patch,
        }
        self.set_params(**kwargs)
        self.patch = None
