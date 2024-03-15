from string import Template
import os

numberOfReplicates = 30
experimentID = input("What is the name of the experiment you're analyzing? ")
updateToAnalyze = input("At which update (multiple of 500) do you want to analyze the population? ")

validTreatments = ["Baseline-Treatment", "Slip-duplicate", "Slip-scramble"]

treatmentParameters = {"Baseline-Treatment" : {"Seed Offset" : 1530, "Slip Mutation Probability" : 0.0, "Slip Fill Mode" : 0},
                       "Slip-duplicate" : {"Seed Offset" : 1590, "Slip Mutation Probability" : 0.05, "Slip Fill Mode" : 0},
                       "Slip-scramble" : {"Seed Offset" : 1710, "Slip Mutation Probability" : 0.05, "Slip Fill Mode" : 0}}

possibleTreatments = os.listdir(f'/scratch/zamanlh_root/zamanlh0/clhaynes/{experimentID}')

for treatmentInQuestion in possibleTreatments:
    if treatmentInQuestion not in validTreatments:
        continue

    else:
        with open('geneDuplicationDataAnalyzerTemplate.sh', 'r') as templateFile:
            templateString = templateFile.read()
            dataAnalysisScriptTemplate = Template(templateString)

        parameters = treatmentParameters[treatmentInQuestion]

        dataAnalysisScriptString = dataAnalysisScriptTemplate.substitute(treatment=treatmentInQuestion,
                                                                        numReplicates=numberOfReplicates,
                                                                        updateAtWhichToAnalyze=updateToAnalyze,
                                                                        seedOffset=parameters["Seed Offset"],
                                                                        divSlipProb=parameters["Slip Mutation Probability"],
                                                                        slipFillMode=parameters["Slip Fill Mode"])

        with open('geneDuplicationDataAnalyzer.sh', 'w') as f:
            f.write(dataAnalysisScriptString)
        
        os.system('bash geneDuplicationDataAnalyzer.sh')

updateToAnalyze