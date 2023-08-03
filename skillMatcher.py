import spacy
from nltk.corpus import stopwords

# EDUCATION = ['ssc','hsc','cbse','icse' 'X', 'XII',
#             'b.e','b.tech','m.e','m.tech','btech','mtech',
#             'diploma','12','12th','10','10th','be','btech'
#             'phd','mphil','mbbs','bachelor','bachelors','master',
#             'masters','inter','intermediate','honors'
#         ]

# STOPWORDS = set(stopwords.words('english'))

#Extract skills(Returns list of skills)
def extract_skills(nlp_text,skill_matcher):
    skills_found = []
    matches = skill_matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        skills_found.append(span.text)

    unique_skills = list(set(skills_found))

    return unique_skills

