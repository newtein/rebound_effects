# Prerequisites 
To access the code files, request an API token from Elsevier by registering at https://dev.elsevier.com/. 


# File descriptions\
The description of all the relevant files is as follows:
## 1. article_full_text.py: Based on the user selection, it fetches the article full-text for ScienceDirect and abstracts for Scopus. 

### Example usage:
a. >python3 article_full_text.py scopus
b. >python3 article_full_text.py science_direct

## 2. article_search.py: Based on the user selection, it fetches the meta-data for ScienceDirect and for Scopus.

## 3. article_search_get_totals.py: Based on the user selection, it fetches the total number of articles indexed. 

## 4. config.py: This file comprises configurations for the searches. 

## 5. science_direct_search_v3.ipynb: Shows an example usage of ArticleContent class in article_full_text.py

## 6. science_direct_temporal_search.ipynb: Get the total number of articles for each year. It uses the temporal_article_search.py file. 

# Visualization files
## 7. search_1_and_2_for_CHI_revisions: File to reproduce the temporal graph in the paper. 
## 8. scopus_plot_temporal_graph_nchi.ipynb/sd_plot_temporal_graph_nchi.ipynb: Plots the temporal graphs (Older version).
##9. plot_word_cloud.py: File to plot the word clouds of the fetched articles. 

Note: The rest of the files are experimental or for exploratory data analysis. These are not required for any aspect of reproducibility. To fetch articles or get totals from science direct or Scopus, use either (1) or (3), though the results will include papers indexed to date (the day searches were conducted). 

