USERNAME=clhaynes
EXPERIMENT_ID=2022-3-29-PaperDuplication

EXPERIMENT_DIR=/scratch/zamanlh_root/zamanlh0/${USERNAME}/${EXPERIMENT_ID}

cp CodingSiteGeneratorHPCCCopy.py ${EXPERIMENT_DIR}

echo "Experiment: ${EXPERIMENT_ID}"
read -p "At which update (multiple of 500) do you want to analyze the population? " ANALYSIS_TIME

python3 RunGeneDuplicationAvidaAnalysisScript.py ${EXPERIMENT_ID} ${ANALYSIS_TIME}

cd ${EXPERIMENT_DIR}

module load gcc/11.2.0
python3 CodingSiteGeneratorHPCCCopy.py ${ANALYSIS_TIME}