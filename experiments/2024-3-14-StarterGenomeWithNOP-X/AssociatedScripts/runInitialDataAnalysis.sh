USERNAME=clhaynes
EXPERIMENT_ID=2024-3-14-StarterGenomeWithNOP-X

EXPERIMENT_DIR=/scratch/zamanlh_root/zamanlh0/${USERNAME}/${EXPERIMENT_ID}

cp $${ASSOCIATED_SCRIPTS_DIR}/CodingSiteGeneratorHPCCCopy.py $${EXPERIMENT_DIR}

ANALYSIS_TIME=`python3 RunGeneDuplicationAvidaAnalysisScript.py`

cd ${EXPERIMENT_DIR}

module load gcc/11.2.0
python3 CodingSiteGeneratorHPCCCopy.py ${ANALYSIS_TIME}