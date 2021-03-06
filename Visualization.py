#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 13:28:27 2021
draw results
@author: jun
"""
import argparse
import os
import torch

from attrdict import AttrDict

from sgan.data.loader import data_loader
from sgan.models import TrajectoryGenerator
from sgan.losses import displacement_error, final_displacement_error
from sgan.utils import relative_to_abs, get_dset_path

import matplotlib.pyplot as plt
import random
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--model_path', default = 'models/sgan-models', type=str)
parser.add_argument('--dataset_name', default='trajectoryP', type=str)
parser.add_argument('--delim', default='tab')
parser.add_argument('--loader_num_workers', default=4, type=int)
parser.add_argument('--obs_len', default=8, type=int)
parser.add_argument('--pred_len', default=8, type=int)
parser.add_argument('--skip', default=1, type=int)
# Optimization
parser.add_argument('--batch_size', default=1, type=int)

def get_generator(checkpoint):
    args = AttrDict(checkpoint['args'])
    generator = TrajectoryGenerator(
        obs_len=args.obs_len,
        pred_len=args.pred_len,
        embedding_dim=args.embedding_dim,
        encoder_h_dim=args.encoder_h_dim_g,
        decoder_h_dim=args.decoder_h_dim_g,
        mlp_dim=args.mlp_dim,
        num_layers=args.num_layers,
        noise_dim=args.noise_dim,
        noise_type=args.noise_type,
        noise_mix_type=args.noise_mix_type,
        pooling_type=args.pooling_type,
        pool_every_timestep=args.pool_every_timestep,
        dropout=args.dropout,
        bottleneck_dim=args.bottleneck_dim,
        neighborhood_size=args.neighborhood_size,
        grid_size=args.grid_size,
        batch_norm=args.batch_norm)
    generator.load_state_dict(checkpoint['g_state'])
    generator.cuda()
    generator.train()
    return generator

def generateFake(args, loader, generator):
    total_traj = 0
    with torch.no_grad():
        for batch in loader:
            batch = [tensor.cuda() for tensor in batch]
            (obs_traj, pred_traj_gt, obs_traj_rel, pred_traj_gt_rel,
             non_linear_ped, loss_mask, seq_start_end) = batch
            #print(obs_traj)
            pred_traj_fake_rel = generator(
                    obs_traj, obs_traj_rel, seq_start_end
                )
            pred_traj_fake = relative_to_abs(
                    pred_traj_fake_rel, obs_traj[-1]
                )

            print(pred_traj_fake)
        return pred_traj_fake

def main(args):
    
    #load generator

    if os.path.isdir(args.model_path):
            filenames = os.listdir(args.model_path)
            filenames.sort()
            paths = [
                os.path.join(args.model_path, file_) for file_ in filenames
            ]
    else:
            paths = [args.model_path]
    for path in paths:
        checkpoint = torch.load(path)
        generator = get_generator(checkpoint)
        
    #generate test data and write to txt file
    for i in range(5):
        x = np.zeros(16)
        y = np.zeros(16)
        #initial position, velocity, direction, curvature, 
        x_0 = random.uniform(-20, 20)
        y_0 = random.uniform(-20, 20)
        v = 1 #velocity
        a = random.randint(0,360)
        a_0 = a #direction
        delta_a = random.randint(-10, 10) #curvature
        for k in range(16):
            #calculate position at t+1
            a_1 = a_0 + delta_a
            x_1 = x_0 + v*np.cos(np.deg2rad(a_1))
            y_1 = y_0 + v*np.sin(np.deg2rad(a_1))
            #record position
            x[k] = x_1
            y[k] = y_1
            #update current position
            x_0 = x_1
            y_0 = y_1
            a_0 = a_1
        
        # Draw point based on above x, y axis values.
        plt.scatter(x, y, s=10, label= "real trajectory", c = 'red')
        # Set chart title.
        plt.title("trajectory generating example, blue is generated, red is real")
        # Set x, y label text.
        plt.xlabel("x")
        plt.ylabel("y")
        plt.xlim(-30, 30)
        plt.ylim(-30, 30)
        plt.grid(True)
        
        f= open("datasets/trajectoryP/vis/trajectory_vis.txt" ,"w+")
    
        for j in range(len(x)):
            f.write(str(16*i + j))
            f.write('\t')
            f.write(str(i))
            f.write('\t')
            f.write(str(round(x[j],6)))
            f.write('\t')
            f.write(str(round(y[j],6)))
            f.write('\n')
        f.close()
        
       
        vis_path = get_dset_path(args.dataset_name, 'vis')

        _, vis_loader = data_loader(args, vis_path)
        
        pred_traj_fake = generateFake(args, vis_loader, generator)
        pred_traj_fake = pred_traj_fake.cpu().numpy().reshape(8,2)
        pred_traj_fake = np.transpose(pred_traj_fake)
        print(pred_traj_fake)
        plt.scatter(pred_traj_fake[0],pred_traj_fake[1],s = 10, label= "generated trajectory", c = 'blue')
        plt.savefig('books_read%i.png' %i)
    
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
    