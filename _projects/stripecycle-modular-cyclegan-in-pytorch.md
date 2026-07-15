---
layout: page
title: "StripeCycle: Modular CycleGAN in PyTorch"
description: "A modular, from-scratch CycleGAN reimplementation in PyTorch for unpaired image-to-image translation — config-driven training, DDP, AMP, and resumable checkpoints."
img: assets/img/projects/stripecycle-logo.png
importance: 5
category: software
github: https://github.com/turhancan97/train-cycleGAN
redirect: https://github.com/turhancan97/train-cycleGAN
docs: https://github.com/turhancan97/train-cycleGAN/blob/main/docs/architecture_and_theory.md
---

**StripeCycle** is a modular, from-scratch reimplementation of [CycleGAN](https://arxiv.org/abs/1703.10593) (Zhu et al., 2017) in PyTorch — built to be read end-to-end and trained on your own data, not used as a black box.

**Overview.** The codebase separates the ResNet generator, PatchGAN discriminator, adversarial + cycle-consistency + identity losses, and image replay buffer into small, readable modules. Training is config-driven (YAML), supports single-node multi-GPU via `DistributedDataParallel`, mixed precision, full resumable checkpoints, and TensorBoard logging (optional Weights & Biases). A generic `UnpairedImageDataset` works with any two image folders; horse2zebra is included as the default benchmark.

- [Repository](https://github.com/turhancan97/train-cycleGAN)
- [Architecture & theory](https://github.com/turhancan97/train-cycleGAN/blob/main/docs/architecture_and_theory.md)
- [Tutorial notebook](https://github.com/turhancan97/train-cycleGAN/blob/main/notebooks/tutorial_cyclegan.ipynb)
