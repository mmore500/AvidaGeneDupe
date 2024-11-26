#!/usr/bin/env python
# coding: utf-8

import numpy
import os


class Treatment():
    def __init__(self,name,params):
        self.name = name
        self.params = params


def getNextRandomSeed():
    with open('/Users/cameronhaynes/Documents/ZE3/currentRandomSeed.txt','r') as f:
        line = f.readlines()
        if(len(line) == 1):
            currentNum = int(line[0])
            return currentNum
        else:
            print("There's no random seed written!")

def writeNextRandomSeed(arrayJobLength = 1):
    currentRandomSeed = getNextRandomSeed()
    with open('/Users/cameronhaynes/Documents/ZE3/currentRandomSeed.txt','w') as f:
        f.writelines(['{}'.format(currentRandomSeed + arrayJobLength)])

    
class sBatchFileArchetype():
    def __init__(self,username,date,experimentID, arrayLength = 1):
        self.username = username
        self.date = date
        self.experimentID = experimentID
        self.arrayLength = arrayLength
    
    def writeFile(self,treatment):
        seedStart = getNextRandomSeed()
        writeNextRandomSeed(self.arrayLength)
        
        defaultIntro = ['#!/bin/bash\n',
                 '# The interpreter used to execute the script\n\n',
                 '#SBATCH --job-name={}{}\n'.format(self.experimentID,treatment.name),
                 '#SBATCH --mail-type=BEGIN,END,FAIL\n',
                 '#SBATCH --mail-user={}@umich.edu\n'.format(self.username),
                 '#SBATCH --nodes=1\n',
                 '#SBATCH --ntasks-per-node=1\n',
                 '#SBATCH --mem=4g\n',
                 '#SBATCH --time=00-04:00:00\n',
                 '#SBATCH --account=zamanlh0\n',
                 '#SBATCH --array=1-{}\n\n'.format(self.arrayLength)]

        lalejiniPreamble = ['USERNAME={}\n'.format(self.username),
                           'EXPERIMENT_ID={}-{}\n'.format(self.date,self.experimentID),
                           'OUTPUT_DIR=/scratch/zamanlh_root/zamanlh0/{}/{}/{}\n'.format('${USERNAME}','${EXPERIMENT_ID}',treatment.name),
                           'CONFIG_DIR=/home/${USERNAME}/AvidaGeneDupe/experiments/${EXPERIMENT_ID}/hpcc/config\n',
                           'SEED_OFFSET={}\n\n'.format(seedStart)]
        
        bulk = ['SEED=$((SEED_OFFSET + SLURM_ARRAY_TASK_ID - 1))\n','JOB_ID=${SLURM_ARRAY_TASK_ID}\n',
                'RUN_DIR=${OUTPUT_DIR}/run_${SEED}\n\n',
                'mkdir -p ${RUN_DIR}\n\n',
                'cd ${RUN_DIR}\n\n',
                "#Don't use the asterisk: actually write everything out so you know what you're working with!\n\n",
                'cp ${CONFIG_DIR}/avida .\n',
                'cp ${CONFIG_DIR}/avida.cfg .\n',
                'cp ${CONFIG_DIR}/default-heads.org .\n',
                'cp ${CONFIG_DIR}/environment.cfg .\n',
                'cp ${CONFIG_DIR}/events.cfg .\n',
                'cp ${CONFIG_DIR}/instset-heads___sensors_NONE.cfg .\n',
                'cp ${CONFIG_DIR}/analyze.cfg .\n\n',
                'EXECUTE="avida -s {} -set COPY_MUT_PROB {} -set COPY_INS_PROB {} -set COPY_DEL_PROB {} -set DIVIDE_INS_PROB {} -set DIVIDE_DEL_PROB {} -set DIVIDE_SLIP_PROB {} -set SLIP_FILL_MODE {}"\n'.format('${SEED}',treatment.params[0],treatment.params[1],treatment.params[2],treatment.params[3],treatment.params[4],treatment.params[5],treatment.params[6]),
                'echo ${EXECUTE} > cmd.log\n',
                './${EXECUTE} > run.log\n',
                './${EXECUTE} -a > analyze.log\n\n',
                'rm avida\n',
                'rm avida.cfg\n',
                'rm default-heads.org\n',
                'rm environment.cfg\n',
                'rm events.cfg\n',
                'rm instset-heads___sensors_NONE.cfg\n',
                'rm analyze.cfg']
        
        with open('{}-{}.sh'.format(self.date,treatment.name),'w') as f:
            f.writelines(defaultIntro)
            f.writelines(lalejiniPreamble)
            f.writelines(bulk)
        print('Finished writing {}-{}.sh'.format(self.date,treatment.name))


Treatments = []
slipDupe = Treatment('Slip-duplicate',[0.0025,0,0,0.05,0.05,0.05,0])
Treatments.append(slipDupe)
slipScramble = Treatment('Slip-scramble',[0.0025,0,0,0.05,0.05,0.05,3])
Treatments.append(slipScramble)
slipNOP = Treatment('Slip-NOP',[0.0025,0,0,0.05,0.05,0.05,1])
Treatments.append(slipNOP)
slipRandom = Treatment('Slip-random',[0.0025,0,0,0.05,0.05,0.05,2])
Treatments.append(slipRandom)
slipScatter = Treatment('Slip-scatter',[0.0025,0,0,0.05,0.05,0.05,5])
Treatments.append(slipScatter)
baseline = Treatment('Baseline-Treatment',[0.0025,0,0,0.05,0.05,0,0])
Treatments.append(baseline)
highMut = Treatment('High-Mutation',[0.0025,0.0075,0.0075,0.05,0.05,0.05,0])
Treatments.append(highMut)


LalejiniEtAlRemix = sBatchFileArchetype('clhaynes','2022-5-21','LalejiniEtAlReplicationHighReplicateCount', 120)
for treat in Treatments:
    LalejiniEtAlRemix.writeFile(treat)

