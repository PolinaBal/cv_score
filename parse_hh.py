import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title.text.strip() if title else "Не указано"

    salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    salary = salary.text.strip() if salary else "Не указано"

    experience = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience.text.strip() if experience else "Не указано"

    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode.text.strip() if employment_mode else "Не указано"

    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company.text.strip() if company else "Не указано"

    location = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location.text.strip() if location else "Не указано"

    description = soup.find("div", {"data-qa": "vacancy-description"})
    description = description.text.strip() if description else "Не указано"

    skills = [
        skill.text.strip()
        for skill in soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})
    ]

    markdown = f"""
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
- {'\n- '.join(skills)}
"""
    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, "html.parser")

    name = soup.find('h2', {'data-qa': 'resume-title'})
    name = name.text.strip() if name else "Не указано"

    gender_age = soup.find('p', {'data-qa': 'resume-personal-gender-age'})
    gender_age = gender_age.text.strip() if gender_age else "Не указано"

    location = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location.text.strip() if location else "Не указано"

    job_title = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title.text.strip() if job_title else "Не указано"

    job_status = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status.text.strip() if job_status else "Не указано"

    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else []

    markdown = f"""
# {name}

**{gender_age}**

**Местоположение:** {location}
**Должность:** {job_title}
**Статус:** {job_status}

## Ключевые навыки
- {', '.join(skills)}
"""
    return markdown.strip()

def get_candidate_info(url: str):
    response = get_html(url)
    if response:
        return extract_candidate_data(response.text)
    return "Ошибка загрузки данных кандидата."

def get_job_description(url: str):
    response = get_html(url)
    if response:
        return extract_vacancy_data(response.text)
    return "Ошибка загрузки данных вакансии."
