import extract_text as extract
import skillMatcher as skills
import pre_processor as preprocess
import Similar as similar
import spacy
from spacy.matcher import PhraseMatcher
import nltk
nltk.download('omw-1.4')
from nltk.tokenize import word_tokenize
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

nlp = spacy.load('en_core_web_sm')
skill_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Load the skills to be matched for Phrase Matching from the all_skills.data
with open('all_skills.data', 'rb') as filehandle:
    # read the data as binary data stream
    all_skills = pickle.load(filehandle)

# Only run nlp.make_doc to speed things up
patterns = list(nlp.tokenizer.pipe(all_skills))
skill_matcher.add("TerminologyList", patterns)

path = './documents/jobDescriptions/Data Scientist.docx'
extension = '.docx'
highest_degree = 'btech'
jobDescription = extract.extract_text(path,extension)
cleaned_jobDescription = preprocess.cleanResume(jobDescription.lower())
nlp_jobDescrption = nlp(cleaned_jobDescription)

jobDescription_skills = set(skills.extract_skills(nlp_jobDescrption,skill_matcher))

resumes_path = './documents/resumes'
eligible_candidates = dict()
eligible = 0
not_eligible = 0

for resume in os.listdir(resumes_path):
    # currently hardcoding highest degree coz of lack of data
    resume_highest_degree = 'btech'
    # initialize expected threshhold 
    threshold_score = 7
    # initialize scores 
    total_score = 0
    skill_match_score = 0
    highest_degree_score = 0
    similarity_score = 0
    resume_extension = '.docx'
    full_resumes_path = resumes_path+'/'+resume 
    resume_text = extract.extract_text(full_resumes_path,resume_extension)
    cleaned_resume_text = preprocess.cleanResume(resume_text.lower())
    nlp_resume_text = nlp(cleaned_resume_text)
    resume_skills = set(skills.extract_skills(nlp_resume_text,skill_matcher))
    match_skills = resume_skills.intersection(jobDescription_skills)

    # Matchings resume skills with job descrption
    # Need to maintain seperate technical and mangerial skills for better results 
    if(len(match_skills) == len(jobDescription_skills)):
        skill_match_score = 3
    
    if(len(match_skills) >= len(jobDescription_skills)/2 ):
        skill_match_score = 1

    # Commenting out due to lack of training data
    # if(highest_degree in cleaned_resume_text):
    #     highest_degree_score = 2
    if( resume_highest_degree == highest_degree):
        highest_degree_score = 2

    similarity_score = similar.match(cleaned_resume_text,cleaned_jobDescription)

    if(similarity_score >= 85):
        similarity_score = 5
    if(similarity_score >= 40 and similarity_score <= 85):
        similarity_score = 1

    total_score = similarity_score+skill_match_score+highest_degree_score

    if(total_score >= threshold_score):
        eligible = eligible+1
        eligible_candidates[resume] = {
            'skills': resume_skills,
            'total_score': total_score
        }
    else:
        not_eligible = not_eligible+1


# Plot the graph
y = np.array([eligible, not_eligible])
mylabels = ['Eligible', 'Not Eligible']
plt.pie(y, labels = mylabels,autopct='%1.1f%%', explode=[0,0.1], shadow=True, startangle=90)
plt.show() 


pprint( dict(sorted(eligible_candidates.items(), key=lambda x: x[1]['total_score'], reverse=True)[:10]))









