(phenotype-organised)=
# Phenotype

(what-is-phenotype)=
## What is phenotype?
Phenotypes are observable traits, which can range from neutral (like height, skin colour, or eye colour) to disabling (e.g. chronic fatigue syndrome) or life-threatening (e.g. cancers), to very specific measurements (e.g. level of calcium in blood).
Since phenotypes can have various levels of specificity, they can also be hierarchical, an individual could display "abnormal muscle morphology", or more specifically "facial muscle atrophy", which means we have to decide at what level to record phenotypes.
Human phenotype information is private information, and some phenotypes are not easy to measure, so information about human phenotypes is not always easy to access.

(proteins-influence-phenotype)=
## How do proteins influence phenotype?
The easiest phenotypes to understand genetically are {ref}`Mendelian<mendel>`. 
In Mendelian phenotypes, a single mutation is responsible for a phenotype, and we can assume that the mutation changes, reduces, or stops entirely the functionality of the protein, and that this protein is the main actor involved in the trait. 
An example of this in humans is the [OPN1MW gene](https://www.genecards.org/cgi-bin/carddisp.pl?gene=OPN1MW) which encodes for green-light absorbing pigment necessary to create green light absorbing cones in the eye: the allele that causes a non-functional OPN1MW gene therefore causes red-green colourblindness. 

The way in which Mendelian genetics affect a phenotype can vary. 
In humans, for a SNP with two alleles, there are three possible *calls*: homozygous wild type (two copies of the most common allele), heterozygous (one copy of the most common allele and one copy of the rarer allele), and homozygous mutant (two copies of the rarer allele). 
Sometimes having one copy of the rarer allele is enough to cause a phenotype, but sometimes two copies are required.
Not all SNPs are disease-causing at all, i.e. have any disease-causing combinations of alleles.

As well as mutations, phenotypes can be caused by chromosomal abnormalities (extra or missing sections of chromosomes). 
In this case, the mechanism is the increased or decreased gene expression of the affected section of the chromosome which is influencing phenotypic differences. 

Proteins can affect the same phenotype indirectly, through protein-protein interaction networks, through interaction with the metabolism (the body's creation of small chemicals, like sugars, fatty acids, and vitamins), and through interaction with the environment of the cell. 
The environment of the cell is of course in turn influenced from the human-scale environment: what we eat, whether we smoke, the air we breathe, and our body's response to outside stimuli.  

[//]: # (TODO: Write a bit more about PPIs/scale-free, etc)

(limits-of-proteins)=
### Limits
For many disease phenotypes (e.g. Breast Cancer, Asbestosis), a genetic mutation might predict an increased probability of having the phenotype, given similar environmental conditions. 
And there are phenotypes which may not be linked to genetic variation at all, but may be entirely influenced by the environment: for example medical conditions that are the result of poisoning. 
In these cases, we might imagine that there is a mutation that humans could have that would prevent or reduce the poison reaction, but since no one has it, we can't study this by looking at human mutations. 

```{margin} Social Constructs
:name: social-constructs
A social construct is an idea or concept that exists because it has been created and agreed upon by society.
```

To get a little philosophical (metaphysical) for just a paragraph, some phenotypes may not even exist. 
That is, they might not be *natural* categories such that there is a straight-forward and physical thing that decides membership to the category{cite}`Fried2017-zu`. 
As an example, consider an imaginary poorly-understood syndrome, it might be diagnosed if you have some of a list of symptoms, but the syndrome might actually be four separate diseases with four totally separate causes and the treatments might only work for one of these diseases. 
Some phenotypes might even be *{ref}`social constructs<social-constructs>`*; there is a long-running debate among psychologists about whether some mental health conditions and other psychological and behavioural concepts are socially constructed{cite}`Hacking1999-gh,Szasz1976-ee`. 
If phenotypes are not based in the physical, then we will likely have difficulty accurately predicting them from genetics.

(ethical-considerations-phenotype)=
### Ethical considerations
Aside from the fact that predicting non-physical concepts is difficult, there are also ethical considerations in trying to predict socially constructed phenotypes.
If we try to predict sexual orientation from genetics {cite}`Kaiser2019-tu`, then we might turn out to be measuring something else which indirectly influences sexual orientation, for example a protein that influences how open people are to new experiences, or something that in turn influences that. 
And in trying to predict intelligence from genetics, for example, we are likely finding associations between variables like how much you have practiced IQ tests or whether you are in the same cultural group as those that created them{cite}`Richardson2002-nx`, reinforcing racist ideas{cite}`Saini_undated-ng`.

(which-phenotypes)=
Even if all phenotypes were natural concepts, predicting the genetic basis of some phenotypes could be harmful{cite}`Schuklenk1997-ag`, for example finding a gay gene could be motivated by, or lead to a search for "treatments" to "cure" homosexuality even if it did have a physical basis. 

Physical measurements can also be problematic for similar reasons.
Take measurements of facial features for example: this brings to mind the image of nazis measuring skulls. 
Where physical measurements are proxies for measuring the social construct of race, these kinds of phenotypes can be similarly worrying.
Facial recognition technology{cite}`Wu2016-ic` is often criticised on this basis{cite}`Stark2018-lk`. 

It is for these reasons, that the majority of modern concepts of phenotype are based in medical concepts, where looking for a link between genotype and phenotype can have a potential life-saving or life-improving benefit.
This scenario still comes with serious ethical considerations, however.
Many disabled people do not want cures for their disabilities{cite}`Pulrang2019-gj`, and people are also worried that the development of genetic screenings for disabilities will effectively result in a genocide of disabled people{cite}`Miller2013-ws`.

(who-gets-the-information)=
Another concern is that people may accidentally find out about phenotypes that they are predisposed to that they do not wish to know about.
This is particularly worrying if there are not any existing preventative/proactive measures to avoid a future diagnosis, and if they are not be able to access genetic counselling. 
For example, 23andMe have a system whereby you must opt-in to viewing reports about your health for some illnesses.

[//]: # (TODO: Add hazard label or link to Snowflake/other sections + spell out that you need to include the people who are affected in the research process.)