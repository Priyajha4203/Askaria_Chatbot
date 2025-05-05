from bs4 import BeautifulSoup
from selenium import webdriver


def extract_clean_text_from_html(file_path):
    # Parse the HTML content
    soup = BeautifulSoup(file_path, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "header", "footer", "noscript", "meta", "link"]):
        tag.decompose()

    # Get visible text
    text = soup.get_text(separator='\n')

    # Clean and filter out empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned_text = "\n".join(lines)
    # print(cleaned_text)
    return cleaned_text


def get_data():
    driver = webdriver.Chrome()
    
    
    urls = ['https://www.acem.edu.in/','https://www.acem.edu.in/director-desk.php', 'http://acem.edu.in/chairman-desk.php' , 
            'https://www.acem.edu.in/vision-mission.php' , 'https://acem.nopaperforms.com/','https://acem.genericsoftware.in/parent/login.aspx',
            'https://www.acem.edu.in/courses-cse.php' , 'https://www.acem.edu.in/courses-cse-aiml.php', 'https://www.acem.edu.in/courses-me.php' , 
            'https://www.acem.edu.in/courses-civil.php','https://www.acem.edu.in/courses-ece.php','https://www.acem.edu.in/courses-bba.php',
            'https://www.acem.edu.in/courses-bba-fsb.php','https://www.acem.edu.in/courses-mba.php','https://www.acem.edu.in/courses-bba-dm.php',
            'https://www.acem.edu.in/courses-bca.php','https://www.acem.edu.in/courses-bca-ds.php','https://acem.genericsoftware.in/onlinereg.aspx',
            'https://www.acem.edu.in/activities-vivrti2025.php','https://www.acem.edu.in/about-us.php', 'https://www.acem.edu.in/approvals.php', 
            'https://www.acem.edu.in/syllabus.php','https://www.acem.edu.in/contact.php', 'https://www.acem.edu.in/blog/ ',
            'https://www.acem.edu.in/placement.php','https://www.acem.edu.in/placement-2024.php', 'https://www.acem.edu.in/nirf/ACEM-NIRF-Engineering-2025.pdf', 
            'https://www.acem.edu.in/activities.php', 'https://www.acem.edu.in/activities-guest-lecture.php',] 

    for i in range(len(urls)):
        driver.get(urls[i])
        
        html_data = driver.page_source
        print("------------------------------------------")
        print("Cheking urls :- " ,urls[i])
        print("------------------------------------------")
        output_path = f"data/website_{i}.txt"
        cleaned_text = extract_clean_text_from_html(html_data)
        
        with open(output_path, "w" , encoding='utf-8') as f:
            f.write(cleaned_text)
        print("✅ Website text extracted and saved to:", output_path)
        
        
      
        
# Save the clean text to a file


if __name__ == "__main__":
    get_data()
