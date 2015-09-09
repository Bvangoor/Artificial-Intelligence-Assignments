The program takes following as the arguments to run :

python ClickStream.py <featurenames> <training_featues> <training_values> <testset_features> <Testset_Values> <threshold_value>

python $Location/ClickStream.py featnames.txt trainfeat.txt trainlabs.txt testfeat.txt testlabs.txt 1


Example 1 :
python ClickStream.py featnames.txt trainfeat.txt trainlabs.txt testfeat.txt testlabs.txt 1

Percentage Accuracy Found : 73.488

python ClickStream.py featnames.txt trainfeat.txt trainlabs.txt testfeat.txt testlabs.txt 0.05

Percentage Accuracy Found : 70.464

python ClickStream.py featnames.txt trainfeat.txt trainlabs.txt testfeat.txt testlabs.txt 0.1

Percentage Accuracy Found : 72.524
