module load gcc/11.2.0

USERNAME=clhaynes
EXPERIMENT_ID=2024-3-14-StarterGenomeWithNOP-X
TREATMENT=$treatment
NUM_REPLICATES=$numReplicates
ANALYSISTIME=$updateAtWhichToAnalyze

EXPERIMENT_DIR=/scratch/zamanlh_root/zamanlh0/$${USERNAME}/$${EXPERIMENT_ID}
OUTPUT_DIR=$${EXPERIMENT_DIR}/$${TREATMENT}
CONFIG_DIR=/home/$${USERNAME}/Documents/AvidaGeneDupe/experiments/$${EXPERIMENT_ID}/hpcc/config
ASSOCIATED_SCRIPTS_DIR=/home/$${USERNAME}/Documents/AvidaGeneDupe/experiments/$${EXPERIMENT_ID}/AssociatedScripts

cp $${ASSOCIATED_SCRIPTS_DIR}/CodingSiteGeneratorHPCCCopy.py $${EXPERIMENT_DIR}

python3 $${ASSOCIATED_SCRIPTS_DIR}/CreateAnalyzeConfig.py $${ANALYSISTIME}

SEED_OFFSET=$seedOffset

for ((iter=0; iter<=NUM_REPLICATES; iter++ ))
do
    SEED=$$(($${iter} + $${SEED_OFFSET}))

    

    RUN_DIR=$${OUTPUT_DIR}/run_$${SEED}

    cd $${RUN_DIR}

    #Don't use the asterisk: actually write everything out so you know what you're working with!

    cp $${CONFIG_DIR}/avida .
    cp $${CONFIG_DIR}/avida.cfg .
    cp $${CONFIG_DIR}/default-headsWithNOP-X.org .
    cp $${CONFIG_DIR}/environment.cfg .
    cp $${CONFIG_DIR}/events.cfg .
    cp $${CONFIG_DIR}/instset-heads___sensors_NONE.cfg .
    cp $${CONFIG_DIR}/analyze.cfg .

    EXECUTE="avida -s $${SEED} -set COPY_MUT_PROB 0.0025 -set COPY_INS_PROB 0.0 -set COPY_DEL_PROB 0.0 -set DIVIDE_INS_PROB 0.05 -set DIVIDE_DEL_PROB 0.05 -set DIVIDE_SLIP_PROB $divSlipProb -set SLIP_FILL_MODE $slipFillMode"
    ./$${EXECUTE} -a > analyze.log

    rm avida
    rm avida.cfg
    rm default-headsWithNOP-X.org
    rm environment.cfg
    rm events.cfg
    rm instset-heads___sensors_NONE.cfg
    rm analyze.cfg

done

cd $${EXPERIMENT_DIR}
python3 CodingSiteGeneratorHPCCCopy.py