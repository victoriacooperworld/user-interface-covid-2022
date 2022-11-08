# covidProject-2022Summer Design

This is the design document for the software for 2022 Summer project design.

### Part 1 - Patient Protein part:

The patient protein program will analyze the input data from patient serum (.fna or .csv) and find the statistically significant ones based on the p values.

Process:
1. Raw sequence using bash script to generate sequences from the blood samples, output FASTA files with the sequences and their frequencies.
2. Remove the non-significant sequences based on the input cut-off table and renew the fasta file.
3. Export a csv file for populations - disease and control.
4. Count the numbers of tetramers from the significant sequences. Use odds ratio to output the significant tetramers.
5. Remove the non-significant tetramers using binomial test.
6. Output the all the tetramers' sequences, corrected p values(Benjamini-Hochberg and Bonferroni).
7. Look up proteins that contain all the significant tetramers.
8. Look for proteins with multiple tetramer "hit", sort by -log(p).
9. Plot protein ID VS decreasing -log(p).
10. Plit individual protein to show location of hits.



