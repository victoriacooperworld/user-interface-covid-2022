from scipy.stats import chisquare
import GenerateDB.STetramerNRlarge as STetramerNRlarge
import PatientInput
import Patient
import numpy as np
def chi(observed_counts_A, observed_counts_B):
    # can we assume anything from our sample
    significance = 0.05
    # what counts did we see in our samples?
    # observed_counts_A = [32, 65, 97, 450]
    # observed_counts_B = [27, 73, 82, 468]
    ########################
    # Get the stat data
    (chi_stat, p_value) = chisquare(observed_counts_A, observed_counts_B)
    # report
    print('chi_stat: %0.5f, p_value: %0.5f' % (chi_stat, p_value))
    if p_value > significance:
        print("Fail to reject the null hypothesis - we have nothing else to say")
    else:
        print("Reject the null hypothesis - suggest the alternative hypothesis is true")

def chi_quality_fit(ob,ex):

    # can we assume anything from our sample
    significance = 0.05

    # what do we expect to see in proportions?
    # expected_proportions = [.05, .1, .15, .7]

    # # what counts did we see in our sample?
    # observed_counts = [27, 73, 82, 468]

    ########################
    # how big was our sample
    sample_size = sum(ob)
    # we derive our comparison counts here for  our expected proportions, based on the sample size
    expected_counts = np.array([float(sample_size) * x for x in ex])
    expected_counts *= sum(ob)/sum(expected_counts)
    # Get the stat data
    (chi_stat, p_value) = chisquare(ob, expected_counts)

    # report
    print('chi_stat: %0.5f, p_value: %0.5f' % (chi_stat, p_value))
      
fnaInputDir = r'Test/Part1TestData/testData0.fna'
input = PatientInput.Input()
data = input.readOneFNAFile(fnaInputDir)
observed, expected = [], []
for d in data:
    observed.append(d[1])
    expected.append(d[2])

print(observed, expected)
chi_quality_fit(observed,expected)





