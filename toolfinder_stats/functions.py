
import re
import pandas as pd


####################################################
### COUNT TOOLS BASED ON SEARCH TERMS & FACILITY ###
####################################################

def facility_counts_by_search_term(search_result, remove_duplicates):

    facility_counts = {}

    tool_list_already_considered = []

    for term in search_result:
        if term not in facility_counts:
            facility_counts[term] = {}
        data = search_result[term]
        nci_count = 0
        nci_if89_count = 0
        pawsey_count = 0
        qris_count = 0
        galaxy_count = 0
        for tool_id in data:
            if remove_duplicates == True:
                if tool_id not in tool_list_already_considered:
                    tool_data = data[tool_id]
                    if tool_data['nci'] == 1:
                        nci_count = nci_count + 1
                    if tool_data['nci_if89'] == 1:
                        nci_if89_count = nci_if89_count + 1
                    if tool_data['pawsey'] == 1:
                        pawsey_count = pawsey_count + 1
                    if tool_data['qris'] == 1:
                        qris_count = qris_count + 1
                    if tool_data['galaxy'] == 1:
                        galaxy_count = galaxy_count + 1
                    tool_list_already_considered.append(tool_id)
            else:
                tool_data = data[tool_id]
                if tool_data['nci'] == 1:
                    nci_count = nci_count + 1
                if tool_data['nci_if89'] == 1:
                    nci_if89_count = nci_if89_count + 1
                if tool_data['pawsey'] == 1:
                    pawsey_count = pawsey_count + 1
                if tool_data['qris'] == 1:
                    qris_count = qris_count + 1
                if tool_data['galaxy'] == 1:
                    galaxy_count = galaxy_count + 1
        facility_counts[term]["nci_count"] = nci_count
        facility_counts[term]["nci_if89_count"] = nci_if89_count
        facility_counts[term]["pawsey_count"] = pawsey_count
        facility_counts[term]["qris_count"] = qris_count
        facility_counts[term]["galaxy_count"] = galaxy_count

    return (facility_counts)


#######################################
### GET TOOLS BASED ON SEARCH TERMS ###
#######################################

def get_tools_that_match_search_terms(search_terms, toolfinder_data):

    search_result = {}

    for term in search_terms:
        if term not in search_result:
            search_result[term] = {}
        for tool_id in toolfinder_data:
            # https://stackoverflow.com/a/49912808
            topics = toolfinder_data[tool_id]["topics"]
            for topic in topics:
                if re.search(term, topic):
                    if tool_id not in search_result[term]:
                        search_result[term][tool_id] = {}
                    if "topic_search_results" not in search_result[term][tool_id]:
                        search_result[term][tool_id]["topic_search_results"] = []
                    search_result[term][tool_id]["topic_search_results"].append(topic)
            publications = toolfinder_data[tool_id]["publications"]
            description = toolfinder_data[tool_id]["description"]
            if re.search(term, publications):
                if tool_id not in search_result[term]:
                    search_result[term][tool_id] = {}
                search_result[term][tool_id]["publication_search_results"] = publications
            #    search_result[term][tool_id]["publication_search_results"].append(publications)
            if re.search(term, description):
                if tool_id not in search_result[term]:
                    search_result[term][tool_id] = {}
                search_result[term][tool_id]["description_search_results"] = description
            if tool_id in search_result[term]:
                nci = toolfinder_data[tool_id]['nci']
                nci_if89 = toolfinder_data[tool_id]['nci_if89']
                pawsey = toolfinder_data[tool_id]['pawsey']
                qris = toolfinder_data[tool_id]['qris']
                galaxy = toolfinder_data[tool_id]['galaxy']
                if nci == '':
                    search_result[term][tool_id]["nci"] = 0
                else:
                    search_result[term][tool_id]["nci"] = 1
                if nci_if89 == '':
                    search_result[term][tool_id]["nci_if89"] = 0
                else:
                    search_result[term][tool_id]["nci_if89"] = 1
                if pawsey == '':
                    search_result[term][tool_id]["pawsey"] = 0
                else:
                    search_result[term][tool_id]["pawsey"] = 1
                if qris == '':
                    search_result[term][tool_id]["qris"] = 0
                else:
                    search_result[term][tool_id]["qris"] = 1
                if galaxy == '':
                    search_result[term][tool_id]["galaxy"] = 0
                else:
                    search_result[term][tool_id]["galaxy"] = 1

    return(search_result)


##########################
### COUNT GALAXY TOOLS ###
##########################

def count_galaxy_tools(toolfinder_csv_from_service):

    galaxy_tool_count = 0

    for idx in toolfinder_csv_from_service:

        galaxy_string = toolfinder_csv_from_service[idx]['Galaxy Australia']
        # https://stackoverflow.com/a/70672659
        # https://stackoverflow.com/a/12595082
        # https://stackoverflow.com/a/4843178
        # https://stackoverflow.com/a/15340694
        match_string_many_tools = "[0-9]+ tools"
        # https://stackoverflow.com/a/49912808
        if pd.isnull(galaxy_string) != True:
            if isinstance(galaxy_string, str):
                if re.search(match_string_many_tools, galaxy_string):
                    # https://stackoverflow.com/a/23986376
                    galaxy_tools_for_this_index = int(galaxy_string.split(" tools")[0])
                    galaxy_tool_count = galaxy_tool_count + galaxy_tools_for_this_index
                else:
                    galaxy_tool_count = galaxy_tool_count + 1

    return galaxy_tool_count


def tidy_toolfinder(toolfinder_dictionary):

    available_data = {}

    for idx in toolfinder_dictionary:
        data = toolfinder_dictionary[idx]
        tool_id = data['Tool identifier (e.g. module name)']
        if tool_id not in available_data:
            available_data[tool_id] = {}
        topics = data['Topic(s)']
        publications = data['Publications']
        # https://stackoverflow.com/a/49912808
        if pd.isnull(topics) != True:
            # https://stackoverflow.com/a/64834756
            topics = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', topics).split(" ")
            available_data[tool_id]["topics"] = topics
        else:
            available_data[tool_id]["topics"] = "Not available"
        if pd.isnull(publications) != True:
            available_data[tool_id]["publications"] = publications
        else:
            available_data[tool_id]["publications"] = "Not available"
        available_data[tool_id]["description"] = data['Description']
        available_data[tool_id]["nci"] = data['NCI (Gadi)']
        available_data[tool_id]["nci_if89"] = data['NCI (if89)']
        available_data[tool_id]["pawsey"] = data['Pawsey (Setonix)']
        available_data[tool_id]["qris"] = data['QRIScloud / UQ-RCC (Bunya)']
        available_data[tool_id]["galaxy"] = data['Galaxy Australia']

    return (available_data)

