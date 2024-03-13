import os

#Used to parse the interesting_tech_companies.md file to get the company name and career page for all the companies
#Write the results to the interesting_tech_companies.txt file

def getCompanyName(companyNameCol):
  start = companyNameCol.find("![") + 2
  end = companyNameCol.find("]",start)
  companyName = companyNameCol[start:end]
  return companyName

def getCompanyCareerLink(companyCareerCol):
  start = companyCareerCol.find("href='") + 6
  end = companyCareerCol.find("'",start)
  careerLink = companyCareerCol[start:end]
  return careerLink



currentFilePath = os.path.dirname(__file__)
markdown_file_path = os.path.join(currentFilePath,'..','interesting_tech_companies.md')

parsedResult = []
with open(markdown_file_path, 'r', encoding='utf-8') as file:
  markup = file.read()
  companies = markup.split('\n')

  for company in companies:
    if not company:
      continue

    companyCols = company.split('|')
    nameCol = companyCols[1]
    careerPageCol = companyCols[4]

    companyName = getCompanyName(nameCol)
    companyCareerLink = getCompanyCareerLink(careerPageCol)

    parsedResult.append(companyName+"|"+companyCareerLink)

txt_file_path = os.path.join(currentFilePath,'..','interesting_tech_companies.txt')
with open(txt_file_path, 'w', encoding='utf-8') as file:
  for company in parsedResult:
    file.write(company+'\n')


    




