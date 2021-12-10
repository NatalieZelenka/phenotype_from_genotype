library(polyester)
library(tidyverse)
library(dplyr)

Sys.setenv('R_MAX_VSIZE'=32000000000) 

# #Load in common genes
fantom_file = '../../data/experiments/fantom/fantom_gene_expression.tsv'
fantom = read.table(fantom_file,sep='\t',header=TRUE, row.names = 1)
fantom <- sapply( fantom, as.numeric )
head(fantom)

num_genes <- 1000
random_seed <- 14052003
set.seed(random_seed)

# Choose a random subsection of genes to focus on 
buffer = 6
gene_sample = sample(nrow(fantom))[1:num_genes+buffer]
sub_samp = fantom[gene_sample,]
zero_rows = sum(rowSums(sub_samp)==0)
sub_samp <- sub_samp[rowSums(sub_samp[])>0,]

#Calculate baseline gene parameters from FANTOM
params <- polyester::get_params(drop_na(data.frame(sub_samp)))
mean <- params$mu  #mean per gene
fit <- params$fit  #fitted relationship between log mean and log size
p0 <- params$p0  #propability of 0 count per gene

print(max(mean))
print(mean(mean))
print(max(p0))

#Load in the experimental design file
mod = read.table('data/simulated/group_mod.csv',sep=',',header=TRUE, row.names = 1)
head(mod)

#Create the simulated count data from log2fold change coeffs and model matrix
coeff_file = 'data/simulated/genes_1000/group_coeffs.csv'
coeffs = data.matrix(read.table(coeff_file, sep=',', header=TRUE, row.names = 1))
head(coeffs)

print(dim(coeffs)[1])
print(length(mean))

simulated_reads <- polyester::create_read_numbers(mean, fit, p0, mod=mod, beta=coeffs,seed=(random_seed))
out_file = 'data/simulated/genes_1000/simulated.csv'
write.csv(simulated_reads,file=out_file)