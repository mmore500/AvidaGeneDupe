from string import Template
import sys

pythonScriptName = sys.argv[0]
updateToAnalyze = sys.argv[1]


with open('../hpcc/config/analyzeTemplate.cfg', 'r') as templateFile:
    templateString = templateFile.read()
    analyzeConfigTemplate = Template(templateString)

analyzeConfigString = analyzeConfigTemplate.substitute(updateAtWhichToAnalyze=updateToAnalyze)

with open('../hpcc/config/analyze.cfg', 'w') as analyzeConfigFile:
    analyzeConfigFile.write(analyzeConfigString)