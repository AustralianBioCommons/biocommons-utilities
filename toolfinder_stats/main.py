
######################################
### TOOLFINDER REPORTING FUNCTIONS ###
######################################

from functions import *

### import ToolFinder CSV, copied from service ###
data = pd.read_csv("./data/ToolFinder_2023_07_07.csv", delimiter=",", keep_default_na = False)
### convert dataframe to a dictionary, as an "index" ###
toolfinder = data.to_dict('index')

##########################
### COUNT GALAXY TOOLS ###
##########################

count_galaxy_tools(toolfinder)

##############################
### TIDY ToolFinder OUTPUT ###
##############################

toolfinder_search_input = tidy_toolfinder(toolfinder_dictionary = toolfinder)

##############
### SEARCH ###
##############

### ASSEMBLY & ALIGNMENT ###

search_terms = [
    "[Aa]ssembly",
    "[Aa]lignment"
]

search_result = get_tools_that_match_search_terms(search_terms, toolfinder_search_input)
assembly_duplicates_removed = facility_counts_by_search_term(search_result, remove_duplicates=True)
assembly_duplicates_included = facility_counts_by_search_term(search_result, remove_duplicates=False)

### ANNOTATION ###
### also need a search for annotation, sequence analysis, gene structure, gene prediction

annotation_search_terms = [
    "[Aa]nnotation",
#    "[Gg]ene ",
#    "[Ss]equence",
#    "[Ss]equence analysis",
    "[Gg]ene structure",
    "[Gg]ene prediction"
]

annotation_search_result = get_tools_that_match_search_terms(annotation_search_terms, toolfinder_search_input)
annotation_duplicates_removed = facility_counts_by_search_term(annotation_search_result, remove_duplicates=True)
annotation_duplicates_included = facility_counts_by_search_term(annotation_search_result, remove_duplicates=False)

