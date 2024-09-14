module load gcc/11.2.0

USERNAME=clhaynes
EXPERIMENT_ID=$experimentalID
TREATMENT=$treatment
NUM_REPLICATES=$numReplicates
ANALYSIS_TIME=$updateAtWhichToAnalyze

EXPERIMENT_DIR=/scratch/zamanlh_root/zamanlh0/$${USERNAME}/$${EXPERIMENT_ID}
OUTPUT_DIR=$${EXPERIMENT_DIR}/$${TREATMENT}
CONFIG_DIR=/home/$${USERNAME}/Documents/AvidaGeneDupe/experiments/$${EXPERIMENT_ID}/hpcc/config
ASSOCIATED_SCRIPTS_DIR=/home/$${USERNAME}/Documents/AvidaGeneDupe/experiments/$${EXPERIMENT_ID}/AssociatedScripts

cd $${ASSOCIATED_SCRIPTS_DIR}

python3 $${ASSOCIATED_SCRIPTS_DIR}/CreateAnalyzeConfig.py $${ANALYSIS_TIME}

SEED_OFFSET=$seedOffset

for ((iter=0; iter<NUM_REPLICATES; iter++ ))
do
    SEED=$$(($${iter} + $${SEED_OFFSET}))

    RUN_DIR=$${OUTPUT_DIR}/run_$${SEED}

    cd $${RUN_DIR}

    mkdir Timepoint_$${ANALYSIS_TIME}

    cp -r data/detail-$${ANALYSIS_TIME}.spop Timepoint_$${ANALYSIS_TIME}
    
    cd Timepoint_$${ANALYSIS_TIME}

    #Don't use the asterisk: actually write everything out so you know what you're working with!

    cp $${CONFIG_DIR}/avida .
    cp $${CONFIG_DIR}/avida.cfg .
    cp $${CONFIG_DIR}/default-heads.org .
    cp $${CONFIG_DIR}/environment.cfg .
    cp $${CONFIG_DIR}/events.cfg .
    cp $${CONFIG_DIR}/instset-heads___sensors_NONE.cfg .
    cp $${CONFIG_DIR}/analyze_$${ANALYSIS_TIME}.cfg .

    EXECUTE="avida -s $${SEED} -set COPY_MUT_PROB 0.0025 -set COPY_INS_PROB 0.0 -set COPY_DEL_PROB 0.0 -set DIVIDE_INS_PROB 0.05 -set DIVIDE_DEL_PROB 0.05 -set DIVIDE_SLIP_PROB $divSlipProb -set SLIP_FILL_MODE $slipFillMode"
    ./$${EXECUTE} -set ANALYZE_FILE analyze_$${ANALYSIS_TIME}.cfg -a > analyze.log

    rm avida
    rm avida.cfg
    rm default-heads.org
    rm environment.cfg
    rm events.cfg
    rm instset-heads___sensors_NONE.cfg
    rm analyze.cfg

done
