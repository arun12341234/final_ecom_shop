from bs4 import BeautifulSoup



def convert_django_html(html_file):
    # Read the contents of the uploaded HTML file to understand its structure
    file_path = html_file

    with open(file_path, "r") as file:
        html_content = file.read()



    # Parse the HTML content and start the conversion
    soup = BeautifulSoup(html_content, 'html.parser')

    # Convert static files paths
    for link in soup.find_all("link"):
        href = link.get("href", "")
        if href and not href.startswith("http"):  # not converting external links
            link["href"] = "{% static '" + href + "' %}"

    for script in soup.find_all("script"):
        src = script.get("src", "")
        if src and not src.startswith("http"):  # not converting external links
            script["src"] = "{% static '" + src + "' %}"

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src and not src.startswith("http"):  # not converting external links
            img["src"] = "{% static '" + src + "' %}"

    # Add the necessary Django template tags for static files and CSRF protection in forms
    # Adding at the beginning of the <head> and <body> respectively
    head = soup.head
    head.insert(0, "{% load static %}")

    body = soup.body
    if soup.find_all("form"):
        body.insert(0, "{% csrf_token %}")

    # Convert the modified HTML content back to a string
    django_template_content = str(soup)

    # Show the first 500 characters of the converted content (as the complete content might be too large)
    django_template_content


    # print(django_template_content)
    django_template_path = 'result_'+file_path

    with open(django_template_path, "w") as file:
        file.write(django_template_content)



import os
import glob

# Specify the directory where you want to search for HTML files
directory_path = ''

# Use the glob module to find HTML files in the specified directory
html_files = glob.glob(os.path.join(directory_path, '*.html'))

# Print the list of HTML files
for html_file in html_files:
    print(html_file)
    convert_django_html(html_file)




