#!/bin/bash

# pick your working env

F_ENV_BIN=/home/olivier/miniconda3/envs/jl/bin

$F_ENV_BIN/isort ../
$F_ENV_BIN/black ../
