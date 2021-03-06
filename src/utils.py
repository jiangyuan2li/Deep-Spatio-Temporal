#!/usr/bin/env python

import torch
from torch import nn

def cal_loss(y_true, y_pred, name='wind_power'):
    y_true = (y_true+1) / 2
    y_pred = (y_pred+1) / 2
    diff = y_true-y_pred
    if name == 'wind_speed':
        diff = diff*40
    mae = []
    rmse = []
    for i in range(y_true.shape[1]):
        x = diff[:, i].detach()
        idx = ~torch.isnan(x)
        l1_x = abs(x[idx]).mean().item()
        l2_x = (x[idx]**2).mean().item()**.5

        mae.append(l1_x)
        rmse.append(l2_x)

    return mae, rmse


def init_weights(m):
    for name, param in m.named_parameters():
        if 'weight' in name:
            nn.init.normal_(param.data, mean=0, std=0.1)
        else:
            nn.init.constant_(param.data, 0)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
