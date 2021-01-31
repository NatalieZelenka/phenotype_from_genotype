import pandas as pd
import numpy as np
from numba import jit


class Fantom:
    def __init__(self, count_file_loc, ensg_mapping_loc,fantom_obo,uberon_obo,sample_info_file_loc):
        """
        Describe class in __init__ section
        
        Attributes:
            attribute1: describe here
            attribute2: describe here
            attribute3: describe here
        """
        # load stuff in:
        self.count_file_loc = count_file_loc
        self.ensg_mapping_loc = ensg_mapping_loc
        self.ensg_mapping = self.load_ensg_mapping()
                
        # transcript expression (sort out samples):
        self.funnel_plot_samples = {}
        self.funnel_plot_transcripts = {}
        
        self.transcript_expression = self.load_counts()
        
        self.col_data, self.rep_info, self.fantom2sample = self.fix_headings()
        self.genes = self.map_to_ensg()
        self.remove_disease_related_samples(fantom_obo)
        self.remove_non_human_samples(fantom_obo)
        self.samples_info = self.load_samples_info(sample_info_file_loc)
        self.remove_non_cell_or_tissue_samples()
        self.tissue_map_ont = self.remove_non_tissue_mappable_samples(fantom_obo)
        self.tissue_map_name = self.check_uberon_by_name(uberon_obo)
        self.tissue_map_overall, self.mapping_disagreements = self.get_overall_tissue_mappings(uberon_obo)
        self.samples = self.transcript_expression.columns[8:]
        
        #gene expression:
        self.gene_expression = self.calculate_gene_expression()
        
    
    @jit
    def calculate_gene_expression(self,gene_expression_method='sum'):
        #NOTE: SLOWWWWWW, numba speeds it up a bit, but it's still slow. Query/eval don't work (easily) with sum or matching strings. Dask seems to slow it down :/
        assert(gene_expression_method in ['sum','mean'])
        
        #quicker to lookup by index. duplicate indices no problem
        transcript_expression = self.transcript_expression
        transcript_expression=transcript_expression.set_index('ensg_id')
        cols_to_drop = transcript_expression.columns[:7]
        transcript_expression=transcript_expression.drop(cols_to_drop,axis=1)
        
        gene_expression = []
        for ensg_id in self.genes:
            per_gene = transcript_expression.loc[[ensg_id]]
                                            
            if gene_expression_method == 'sum':
                row = list(per_gene.sum(axis=0,skipna=True,min_count=1))
                                          
            elif gene_expression_method == 'mean':
                row = list(per_gene.mean(axis=0,skipna=True,min_count=1))
            gene_expression.append(row)
        self.funnel_plot_transcripts['genes'] = len(gene_expression)
        return pd.DataFrame(gene_expression,index = self.genes,columns = self.samples)
    
    def load_ensg_mapping(self):
        # load HGNC to ENSG mappings (downloaded from Biomart)
        hgnc_ensg = pd.read_csv(self.ensg_mapping_loc,delimiter='\t')
        hgnc_ensg.set_index('HGNC ID',inplace=True)
        hgnc_ensg = hgnc_ensg[~hgnc_ensg.index.duplicated(keep=False)]
        return hgnc_ensg
    
    def map_to_ensg(self):
        ensg_ids = []
        unmapped_counter = 0
        multigene_counter = 0
        for i, row in self.transcript_expression.iterrows():
            hgnc_ids = row['hgnc_id'].split(' ')

            if len(hgnc_ids)>1:
                ensg_ids.append(np.nan)
                multigene_counter +=1
                continue

            try:
                ensg_id = self.ensg_mapping.loc[hgnc_ids[0]]['Gene stable ID']
                ensg_ids.append(ensg_id)
            except:
                ensg_ids.append(np.nan)
                unmapped_counter+=1
                
        self.funnel_plot_transcripts['transcripts mapped by biomart'] =  self.transcript_expression.shape[0] -unmapped_counter
        self.funnel_plot_transcripts['transcripts map to exactly one gene'] = self.transcript_expression.shape[0] -unmapped_counter - unmapped_counter - multigene_counter
        
        self.transcript_expression.insert(0,'ensg_id',pd.Series(ensg_ids ,index = self.transcript_expression.index))
        self.transcript_expression.dropna(subset=['ensg_id'],inplace=True)

        ensg_ids = list(set(ensg_ids))
        
        return pd.Series(ensg_ids).dropna()
        
    def load_counts(self):
        """
        Returns:
            transcript_expression: pandas dataframe containing transcript expression
        """
        #load file:
        transcript_expression = pd.read_csv(self.count_file_loc,delimiter='\t',comment='#')
        transcript_expression.drop([0], axis='index', inplace = True)
        self.funnel_plot_samples['all samples'] = transcript_expression.shape[1]
        self.funnel_plot_transcripts['all transcripts'] = transcript_expression.shape[0]
        
        #drop transcripts without a gene annotation:
        transcript_expression.dropna(subset=['hgnc_id'],inplace=True)
        self.funnel_plot_transcripts['transcripts mapped by fantom'] = transcript_expression.shape[0]
                
        return transcript_expression
    
    def fix_headings(self):
        """
        Original columns of FANTOM counts file contain lots of additional information, we relabel to just the accession numbers and save the additional column data in a pandas dataframe (col_data)
        """
        
        rep_info = []
        old_columns = self.transcript_expression.columns
        new_columns = []
        tech_rep_counter = 0
        bio_rep_counter = 0
        fantom2sample = []
        for col_name in old_columns[7:]:
            fantom_sample_accession = 'FF:'+col_name.split('.')[3]
            original_fantom=fantom_sample_accession
            
            if 'tech_rep' in col_name:
                number = col_name.split('tech_rep')[-1][0] #first character after 'tech_rep' (e.g. "1" or "2")
                fantom_sample_accession = fantom_sample_accession + '_tech_rep' + number
                if number == '1':
                    tech_rep_counter += 1
                tech_rep_id = 'FANTOM-T' + str(tech_rep_counter).zfill(3)
            else:
                tech_rep_id = None
                
            if 'biol_rep' in col_name:
                number = col_name.split('biol_rep')[-1][0] #first character after 'bio_rep' (e.g. "1" or "2")
                if number == '1':
                    bio_rep_counter +=1
                bio_rep_id = 'FANTOM-B' + str(bio_rep_counter).zfill(3)
            else:
                bio_rep_id = None
            
            fantom2sample.append([original_fantom, fantom_sample_accession])
            rep_info.append([fantom_sample_accession, tech_rep_id, bio_rep_id])
            new_columns.append(fantom_sample_accession)
        
        fantom2sample = pd.DataFrame(fantom2sample, columns=['Sample ID', 'Fantom Accession Number'])
        fantom2sample.set_index('Sample ID', inplace=True)
        rep_info = pd.DataFrame(rep_info, columns=['Sample ID', 'Tech Rep ID', 'Bio Rep ID'])
        rep_info.set_index('Sample ID', inplace = True)
        
        self.transcript_expression.columns = list(old_columns)[:7] + new_columns
        col_data = pd.DataFrame(old_columns[7:],index = new_columns)
        
        return col_data, rep_info, fantom2sample

    def load_samples_info(self, sample_info_file_loc):
        samples_info = pd.read_csv(sample_info_file_loc, index_col=1)
        return samples_info

    def fantom_to_sample(self, fantom_ids):
        samples = []
        for fantom_id in fantom_ids:
            for sample in self.fantom2sample['Fantom Accession Number'].loc[[fantom_id]]:
                samples.append(sample)
        return samples
    
    def remove_non_cell_or_tissue_samples(self):
        bad_categories = list(
            set([x.split('_')[0] for x in self.transcript_expression.columns])
            &
            set(self.samples_info[~self.samples_info['Characteristics [Category]'].isin(['tissues', 'primary cells'])].index)
        )
        self.transcript_expression.drop(self.fantom_to_sample(bad_categories), axis='columns', inplace=True)

        time_courses = list(
            set([x.split('_')[0] for x in self.transcript_expression.columns])
            &
            set(self.samples_info[self.samples_info['Characteristics [Category]'] == 'time courses'].index)
        )
        self.transcript_expression.drop(time_courses, axis='columns', inplace=True)
        
        frac_and_per = list(
            set([x.split('_')[0] for x in self.transcript_expression.columns])
            &
            set(self.samples_info[self.samples_info['Characteristics [Category]'] == 'fractionations and perturbations'].index)
        )
        self.transcript_expression.drop(frac_and_per, axis='columns', inplace=True)
        
        self.funnel_plot_samples['cell differentiation, cell line, unlabelled samples removed'] = self.transcript_expression.shape[1]

    def remove_disease_related_samples(self,obo):
        disease_relations_of_interest = ['is_a','is_model_for']
        disease_relations = obo.get_relations(disease_relations_of_interest,[x.split('_')[0] for x in self.transcript_expression.columns[8:]],'DOID',obo.ont)
        disease_related = disease_relations.relations.dropna().index
        self.transcript_expression.drop(self.fantom_to_sample(disease_related), axis='columns', inplace = True)
        self.funnel_plot_samples['disease-related samples removed'] = self.transcript_expression.shape[1]
        
    def remove_non_human_samples(self,obo):
        human_relations_of_interest = ['is_a']
        human_relations = obo.get_relations(human_relations_of_interest,[x.split('_')[0] for x in self.transcript_expression.columns[8:]],'FF:0000210',obo.ont)
        non_human = pd.isna(human_relations.relations[0])[pd.isna(human_relations.relations[0])==True].index
        self.transcript_expression.drop(self.fantom_to_sample(non_human), axis='columns',inplace = True)
        self.funnel_plot_samples['non-human samples removed'] = self.transcript_expression.shape[1]
        
    def remove_non_tissue_mappable_samples(self,obo):
        #TODO: check mapping against fantom sample info.
        tissue_relations_of_interest = ['is_a','related_to','part_of','derives_from','intersection_of','union_of']
        tissue_relations = obo.get_relations(tissue_relations_of_interest,[x.split('_')[0] for x in self.transcript_expression.columns[8:]], 'UBERON',obo.ont)
        
        tissue_map_ont = []
        for index, row in tissue_relations.relations.iterrows():
            relation_string = row[0]
            if pd.isna(relation_string):
                uberon = None
            else:
                uberon = relation_string.split('_')[-1]
            tissue_map_ont.append([index,relation_string,uberon])
        tissue_map_ont = pd.DataFrame(tissue_map_ont,columns = ['FANTOM','Relation String','UBERON'])
        tissue_map_ont = tissue_map_ont.set_index('FANTOM')
        unmappable = tissue_map_ont[pd.isna(tissue_map_ont['UBERON'])]
        self.transcript_expression.drop(self.fantom_to_sample(unmappable.index), axis = 'columns', inplace = True)
        tissue_mapping = tissue_relations.relations
        self.funnel_plot_samples['unmapped tissues removed'] = self.transcript_expression.shape[1]

        return tissue_map_ont
        
    def check_uberon_by_name(self,uberon_obo,default=None):
        uberon_obo = uberon_obo.ont
        #MAPPING BY NAME:
        samples_info = self.samples_info.loc[list([x.split('_')[0] for x in self.transcript_expression.columns[8:]])] #limits to things we currently are considering as samples
        samples_names = pd.DataFrame(samples_info['Characteristics[Tissue]']).rename(columns = {'Characteristics[Tissue]':'tissue name'}).dropna()
        
        name2uberon = []
        for fantom_term, row in samples_names.iterrows():
            tissue_name = row['tissue name']
            found = False
            tissue_name = tissue_name.lower()
            for uberon_term in uberon_obo.keys():
                try:
                    synonyms = uberon_obo[uberon_term]['synonyms']
                except:
                    synonyms = []
                if (uberon_obo[uberon_term]['name'].lower() == tissue_name) or (tissue_name in synonyms):
                    name2uberon.append([fantom_term,uberon_term,tissue_name])
                    found = True
            if found == False:
                name2uberon.append([fantom_term,None,tissue_name])

        name2uberon = pd.DataFrame(name2uberon, columns = ['FANTOM','UBERON','name matched on'])
        name2uberon=name2uberon.set_index('FANTOM')
        return name2uberon
    
    def get_overall_tissue_mappings(self,uberon_ont):
        samples_info = self.samples_info.loc[list([x.split('_')[0] for x in self.transcript_expression.columns[8:]])] #limits to things we currently are considering as samples
        samples_names = pd.DataFrame(samples_info['Characteristics[Tissue]']).rename(columns = {'Characteristics[Tissue]':'tissue name'}).dropna()
        
        unmappable_by_name = self.tissue_map_name[pd.isna(self.tissue_map_name['UBERON'])]
        mappable_by_name = self.tissue_map_name.dropna(subset=['UBERON'])
        
        unmappable_by_ont = self.tissue_map_ont[pd.isna(self.tissue_map_ont['UBERON'])]
        mappable_by_ont = self.tissue_map_ont.dropna(subset=['UBERON'])

        relations_of_interest = ['is_a','part_of']
        overall_mapping = []
        disagreements = []
        unmappable = []
        for sample in self.transcript_expression.columns[8:]:    
            #check if mappable by name:
            try:
                by_name = mappable_by_name.loc[[sample.split('_')[0]]].drop_duplicates()['UBERON'][0]
                name_matched_on = mappable_by_name.loc[[sample.split('_')[0]]].drop_duplicates()['name matched on'][0]
            except:
                by_name = None
                name_matched_on = None

            #check if mappable by ontology:
            try:
                by_ont = mappable_by_ont.loc[[sample]].drop_duplicates()['UBERON'][0]
                relation_string = mappable_by_ont.loc[[sample]].drop_duplicates()['Relation String'][0]
                name_string = relation_string_2_name_string(relation_string,fantom_obo.ont)
            except:
                by_ont = None
                relation_string = None
                name_string = None
    
            #if mappable by one and not the other:
            if by_name and not by_ont:
                overall = by_name
                mapped_using = "name"
            elif by_ont and not by_name:
                overall = by_ont
                mapped_using = "ontology"
            #if not mappable by either:
            elif not by_name and not by_ont:
                unmappable.append([sample])
                mapped_using = None
            #if mappable by both:
            else:
                #if map to the same ID:
                if by_name==by_ont:
                    overall=by_ont
                    mapped_using = "both (same)"
                #if map to different IDs:
                elif by_name!=by_ont:
                    one_way = uberon_obo.Relations(relations_of_interest,[by_name],by_ont,uberon_obo.ont)
                    other_way = uberon_obo.Relations(relations_of_interest,[by_ont],by_name,uberon_obo.ont)
                    #If no relationship between the mapped IDs:
                    if pd.isna(one_way.relations[0][0]) and pd.isna(other_way.relations[0][0]):
                        disagreements.append([sample,by_name,by_ont,relation_string,samples_names.loc[sample]['tissue name']])
                        overall=by_name
                        mapped_using = "name"
                    #If one is (part of) another:
                    elif pd.isna(one_way.relations[0][0]) and not pd.isna(other_way.relations[0][0]):
                        overall = by_name
                        mapped_using = "name"
                        print("name",other_way.relations[0][0])
                    elif not pd.isna(one_way.relations[0][0]) and pd.isna(other_way.relations[0][0]):
                        overall = by_ont
                        mapped_using = "ontology"
                        print("ont",one_way.relations[0][0])

            overall_mapping.append([sample,by_name,by_ont,relation_string,name_matched_on,name_string,overall,mapped_using])
        
        #Make the overall mapping
        overall_mapping = pd.DataFrame(overall_mapping,columns = ['Sample ID','by name','by ont','relation string','name label', 'name string','overall','mapped by'])
        overall_mapping.set_index('Sample ID', inplace=True)
        #Remove overly general tissues (e.g. "tissue","anatomical entity",embryo")
        too_general = ['UBERON:0000061','UBERON:0000479','UBERON:0000467','UBERON:0011216','UBERON:0000922']
        too_general_samples = overall_mapping[overall_mapping['overall'].isin(too_general)]
        overall_mapping = overall_mapping[~overall_mapping['overall'].isin(too_general)]
        overall_mapping.dropna(subset=['overall'],inplace=True)
        self.transcript_expression.drop(too_general_samples.index, axis='columns', inplace = True)
        self.funnel_plot_samples['overly general tissues removed'] = self.transcript_expression.shape[1]

        
        #Format/sort disagreements matrix:
        disagreements = pd.DataFrame(disagreements,columns = ['FANTOM','by name', 'by ont','relation string','name label'])
        pairs = pd.DataFrame(disagreements,columns = ['by name','by ont'])
        pairs = pairs.set_index('by name').drop_duplicates()

        disagreements = disagreements.set_index('by name')
        disagreements = disagreements.loc[pairs.index]
        disagreements = disagreements.drop_duplicates(subset=['by ont'], keep='first')
        # disagreements.set_index('FANTOM')
        name_strings = []
        for sample in disagreements['FANTOM']:
            index = disagreements[disagreements['FANTOM']==sample].index[0]
            relation_string = disagreements[disagreements['FANTOM']==sample].loc[index,'relation string'][0]
            name_string = relation_string_2_name_string(relation_string,fantom_obo.ont)
            name_strings.append(name_string)
        disagreements.loc[:,'name string'] = pd.Series(name_strings,index=disagreements.index)
        
        return overall_mapping, disagreements
