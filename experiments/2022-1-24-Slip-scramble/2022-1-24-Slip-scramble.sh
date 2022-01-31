#!/bin/bash
# The interpreter used to execute the script

#SBATCH --job-name=AvidaGeneDupe_Slip-scramble
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=clhaynes@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=4g
#SBATCH --time=00-04:00:00
#SBATCH --account=zamanlh0
#SBATCH --array=1-30

# -- I like to define helpful variables up top --
USERNAME=clhaynes
EXPERIMENT_ID=2022-1-24-Slip-scramble

OUTPUT_DIR=/scratch/zamanlh_root/zamanlh0/${USERNAME}
CONFIG_DIR=/home/${USERNAME}/AvidaGeneDupe/experiments/${EXPERIMENT_ID}/hpcc/config

SEED_OFFSET=1000
SEED=$((SEED_OFFSET + SLURM_ARRAY_TASK_ID - 1))

JOB_ID=${SLURM_ARRAY_TASK_ID}

RUN_DIR=${OUTPUT_DIR}/run_${SEED}

mkdir -p ${RUN_DIR}

cd ${RUN_DIR}

#Don't use the asterisk: actually write everything out so you know what you're working with!

cp ${CONFIG_DIR}/* .

EXECUTE="avida -s ${SEED}"
echo ${EXECUTE} > cmd.log
./${EXECUTE} > run.log
./${EXECUTE} -a > analyze.log

rm avida
rm avida.cfg
rm default-heads.org
rm environment.cfg
rm events.cfg
rm instset-heads___sensors_NONE.cfg
rm analyze.cfg