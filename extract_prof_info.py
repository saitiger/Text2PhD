from bs4 import BeautifulSoup
import requests

def extract_prof_info(url):
    #  get the html content
    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting name
    try:
        name = soup.find('h4', class_='facultyname').text

        # Extracting position
        position = soup.find('div', class_='education-piece').find('p').text

        # Extracting biography
        try:
            biography_header = soup.find('div', class_='biography-piece').find('h4').text
            biography_text = soup.find('div', class_='biography-piece').text[len(biography_header):].strip()
            research_summary = soup.find('div', class_='research-piece').text
            research_summary = ' '.join(research_summary.split()[:100])
        except:
            biography_text = ""
            research_summary = ""
        
        # print(f"{'Name:':<20}{name}")
        # print(f"{'Position:':<20}{position}")
        # print(f"{'Biography:':<20}{biography_text[:50]}...")
        # print(f"{'Research Summary:':<20}{repr(research_summary)[:50]}...")
        structure = {
            'position': position,
            'biography': biography_text,
            'research_summary': research_summary
        }
        return (name,structure)
    
    except:
        return

# main function
if __name__ == "__main__":
    url = f"https://viterbi.usc.edu/directory/faculty/Barnhart/David"
    extract_prof_info(url)
    print()