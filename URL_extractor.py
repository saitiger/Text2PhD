import requests
from bs4 import BeautifulSoup
from extract_prof_info import extract_prof_info
from scholarly import scholarly
import re


def validate_profs(profs):
    validated_profs = []
    pattern = r'university of southern california|usc'
    for name in profs:
        try :
            search_query = scholarly.search_author(name)
            # Retrieve the first result from the iterator
            first_author_result = next(search_query)
            author = scholarly.fill(first_author_result, sections=['basics', 'publications'])

            if re.search(pattern,author['affiliation'].lower()):
                validated_profs.append(name)
        except:
            pass

    return validated_profs

def create_validated_auths(validated_profs):
    validated_author_ls = []
    for name in validated_profs:
        search_query = scholarly.search_author(name)
        # Retrieve the first result from the iterator
        first_author_result = next(search_query)

        # Retrieve all the details for the author
        validated_author_ls.append((name,scholarly.fill(first_author_result, sections=['basics', 'publications'])))
        # recent_publications = author['publications']
    return validated_author_ls

def scholar_scraper(names):
    validated_profs = validate_profs(names)
    validated_author_ls = create_validated_auths(validated_profs)
    
    google_scholar_data = {}
    for name,author_details in validated_author_ls:
        publications = []
        interests = author_details["interests"]
        for publication in author_details["publications"]:
            if "pub_year" in publication['bib'].keys():
                publications.append((publication['bib']['title'],int(publication['bib']['pub_year'])))


        publications = sorted(publications, key=lambda x: x[1], reverse=True)
        pub_text = ""
        for i in publications[:10]:
            pub_text += "Title: " + i[0]+", "+str(i[1])+ "\n"
          
        interest_text = ""
        for i in interests:
            interest_text += "## " + i + "\n"
        
        google_scholar_data[name] = {"interests":interest_text,"publications":pub_text}
    
    return google_scholar_data



def extract_professor_urls(base_url):
    """
    Extract professor URLs from the given Faculty Directory webpage.
    """
    # Send a GET request to the URL
    response = requests.get(base_url)
    response.raise_for_status()  # Raise exception if the request failed

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all professor URLs
    professor_urls = []
    for anchor in soup.select('a h5.resultName'):
        if anchor.parent.has_attr('href'):
            professor_urls.append("https://viterbi.usc.edu" + anchor.parent['href'])

    return professor_urls

def get_all_prof_tuples(limit=float('inf')):
    base_url = 'https://viterbi.usc.edu/directory/faculty/'
    professor_urls = extract_professor_urls(base_url)
    prof_tuples = [extract_prof_info(url) for url in professor_urls[:limit]]
    prof_tuples = [i for i in prof_tuples if i is not None]

    prof_tuples = {i[0]:i[1] for i in prof_tuples}
    
    names = list(prof_tuples.keys())

    scholar_data = scholar_scraper(names)
    print(scholar_data)
    for name in names:
        if name in scholar_data:
            for key in scholar_data[name].keys():
                prof_tuples[name][key] = scholar_data[name][key]

    # print(scholar_data)
    # for i in prof_tuples:
    #     print()
    #     print(i)
    return prof_tuples

if __name__ == "__main__":
    prof_tuples = get_all_prof_tuples(limit=750)
    for k,v in prof_tuples.items():
        markdown_str = ''
        for key, value in v.items():
            markdown_str += f"{'#' * 1} {key}\n\n{value}\n\n"

        with open(f'./Prof_info_docs/{k}.txt',"w+") as f:
            f.write(markdown_str)
            
        
    print(len(prof_tuples))