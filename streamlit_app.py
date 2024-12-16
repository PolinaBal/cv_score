import os
import streamlit as st
import openai
from parse_hh import get_candidate_info, get_job_description

# OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# System prompt
SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу.
Потом представь результат в виде оценки от 1 до 10.
""".strip()

# Function to call GPT

def request_gpt(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Correct model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1000,
            temperature=0,
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.BadRequestError as e:
        return f"Bad request: {e}"
    except openai.error.AuthenticationError as e:
        return f"Authentication error: {e}"
    except openai.error.APIConnectionError as e:
        return f"Connection error: {e}"
    except openai.error.RateLimitError as e:
        return f"Rate limit exceeded: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Streamlit interface
st.title("CV Scoring App")

job_description_url = st.text_area("Enter the job description URL")
cv_url = st.text_area("Enter the CV URL")

if st.button("Score CV"):
    if not job_description_url or not cv_url:
        st.error("Please fill out both fields!")
    else:
        with st.spinner("Scoring CV..."):

            job_description = get_job_description(job_description_url)
            cv = get_candidate_info(cv_url)

            st.write("**Job Description:**")
            st.write(job_description)

            st.write("**CV:**")
            st.write(cv)

            user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
            response = request_gpt(SYSTEM_PROMPT, user_prompt)

        if "error" in response.lower():
            st.error(response)
        else:
            st.success("CV scored successfully!")
            st.write("**Response from GPT:**")
            st.write(response)


        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
        response = request_gpt(SYSTEM_PROMPT, user_prompt)

    st.write(response)
