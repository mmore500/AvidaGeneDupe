#!/bin/bash
# The interpreter used to execute the script

#SBATCH --job-name=2022-5-5-LalejiniEtAlWLogic25DoubleKnockoutDataTidying
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=clhaynes@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=8g
#SBATCH --time=00-08:00:00
#SBATCH --account=zamanlh1
#SBATCH --array=1

USERNAME=clhaynes
EXPERIMENT_ID=2022-5-5-LalejiniEtAlWLogic25
INPUT_DIR=/scratch/zamanlh_root/zamanlh0/${USERNAME}/${EXPERIMENT_ID}

cd ${INPUT_DIR}

#Don't use the asterisk: actually write everything out so you know what you're working with!

cp /home/${USERNAME}/AvidaGeneDupe/experiments/${EXPERIMENT_ID}/AssociatedScripts/DoubleKnockoutDataTidier.py ${INPUT_DIR} 
python DoubleKnockoutDataTidier.py > pythonOutput.log

