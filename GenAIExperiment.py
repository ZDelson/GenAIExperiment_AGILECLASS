import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, request, send_file
from io import StringIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        program_data = extract_program_data(url)
        if program_data:
            csv_data = convert_to_csv(program_data)
            return send_file(
                StringIO(csv_data),
                as_attachment=True,
                attachment_filename='program_data.csv',
                mimetype='text/csv'
            )
        else:
            return "Error extracting program data. Please check the URL and try again."
    return """
        <form method="post">
            <label for="url">Enter YMCA Program Search URL:</label><br>
            <input type="text" id="url" name="url" value="https://www.ymcachicago.org/programs">
            <input type="submit" value="Download Program Data">
        </form>
    """

def extract_program_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        program_data = []
        for row in soup.find_all('tr')[1:]:
            columns = row.find_all('td')
            program_data.append({
                'Folder_Name': columns[0].text.strip(),
                'Program_Name': columns[1].text.strip(),
                'Program_Description': columns[2].text.strip(),
                'Logo_URL': columns[3].find('img')['src'].strip(),
                'Category': columns[4].text.strip(),
                'Program_Capacity': columns[5].text.strip(),
                'Min_Age': columns[6].text.strip(),
                'Max_Age': columns[7].text.strip(),
                'Meeting_Type': columns[8].text.strip(),
                'Location_Name': columns[9].text.strip(),
                'Address': columns[10].text.strip(),
                'City': columns[11].text.strip(),
                'State': columns[12].text.strip(),
                'Zipcode': columns[13].text.strip(),
                'Program_URL': columns[14].find('a')['href'].strip(),
                'Registration_URL': columns[15].find('a')['href'].strip(),
                'Start_Date': columns[16].text.strip(),
                'End_Date': columns[17].text.strip(),
                'Start_Time': columns[18].text.strip(),
                'End_Time': columns[19].text.strip(),
                'Registration_Deadline': columns[20].text.strip(),
                'Contact_Name': columns[21].text.strip(),
                'Contact_Email': columns[22].text.strip(),
                'Contact_Phone': columns[23].text.strip(),
                'Price': columns[24].text.strip(),
                'Extra_Data': columns[25].text.strip(),
                'online_address': columns[26].text.strip(),
                'dosage': columns[27].text.strip(),
                'internal_id': columns[28].text.strip(),
                'neighborhood': columns[29].text.strip(),
                'community': columns[30].text.strip(),
                'ward': columns[31].text.strip()
            })
        return program_data
    else:
        return None

def convert_to_csv(program_data):
    df = pd.DataFrame(program_data)
    csv_data = df.to_csv(index=False)
    return csv_data

if __name__ == '__main__':
    app.run(debug=True)
