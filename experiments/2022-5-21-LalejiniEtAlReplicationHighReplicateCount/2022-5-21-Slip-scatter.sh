#!/bin/bash
# The interpreter used to execute the script

#SBATCH --job-name=LalejiniEtAlReplicationHighReplicateCountSlip-scatter
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=clhaynes@umich.edu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=4g
#SBATCH --time=00-08:00:00
#SBATCH --account=zamanlh0
#SBATCH --array=1-120

USERNAME=clhaynes
EXPERIMENT_ID=2022-5-21-LalejiniEtAlReplicationHighReplicateCount
OUTPUT_DIR=/scratch/zamanlh_root/zamanlh0/${USERNAME}/${EXPERIMENT_ID}/Slip-scatter
CONFIG_DIR=/home/${USERNAME}/AvidaGeneDupe/experiments/${EXPERIMENT_ID}/hpcc/config
SEED_OFFSET=2850

SEED=$((SEED_OFFSET + SLURM_ARRAY_TASK_ID - 1))
JOB_ID=${SLURM_ARRAY_TASK_ID}
RUN_DIR=${OUTPUT_DIR}/run_${SEED}

mkdir -p ${RUN_DIR}

cd ${RUN_DIR}

#Don't use the asterisk: actually write everything out so you know what you're working with!

cp ${CONFIG_DIR}/avida .
cp ${CONFIG_DIR}/avida.cfg .
cp ${CONFIG_DIR}/default-heads.org .
cp ${CONFIG_DIR}/environment.cfg .
cp ${CONFIG_DIR}/events.cfg .
cp ${CONFIG_DIR}/instset-heads___sensors_NONE.cfg .
cp ${CONFIG_DIR}/analyze.cfg .

EXECUTE="avida -s ${SEED} -set COPY_MUT_PROB 0.0025 -set COPY_INS_PROB 0 -set COPY_DEL_PROB 0 -set DIVIDE_INS_PROB 0.05 -set DIVIDE_DEL_PROB 0.05 -set DIVIDE_SLIP_PROB 0.05 -set SLIP_FILL_MODE 5"
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