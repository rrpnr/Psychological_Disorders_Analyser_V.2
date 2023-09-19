import streamlit as st
import openai
import os
import random
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

# Streamlit App
st.set_page_config(
    page_title="Psychological Disorders Analyser V.2:green_heart:",
    page_icon=":green_heart:",
    layout="wide"
)

st.title('Psychological Disorders Analyser V.2:green_heart:')

OPEN_API_KEY = st.text_input('Enter API key', type="password")

if st.button('Generate'):
    if not OPEN_API_KEY.strip():
        st.write("Please provide the missing fields.")
    else:
        try:
            os.environ['OPENAI_API_KEY'] = OPEN_API_KEY
            openai.api_key = OPEN_API_KEY

            disorder_set = {'Intellectual Disability', 'Global Developmental Delay', 'Unspecified Intellectual Disability', 'Language Disorder Speech Sound Disorder', 'Childhood-Onset Fluency Disorder', 'Social Communication Disorder', 'Unspecified Communication Disorder', 'Autism Spectrum Disorder', 'Attention-Deficit/Hyperactivity Disorder', 'Other Specified Attention-Deficit/Hyperactivity Disorder', 'Unspecified Attention-Deficit/Hyperactivity Disorder', 'Specific Learning Disorder', 'Developmental Coordination Disorder', 'Stereotypic Movement Disorder', 'Tic Disorders', 'Tourette’s Disorder','Persistent (Chronic) Motor or Vocal Tic Disorder', 'Provisional Tic Disorder', 'Other Specified Tic Disorder', 'Unspecified Tic Disorder', 'Other Specified Neurodevelopmental Disorder', 'Unspecified Neurodevelopmental Disorder', 'Schizotypal (Personality) Disorder', 'Delusional Disorder', 'Brief Psychotic Disorder', 'Schizophreniform Disorder', 'Schizophrenia', 'Schizoaffective Disorder', 'Substance/Medication-Induced Psychotic Disorder', 'Psychotic Disorder Due to Another Medical Condition', 'Catatonia Associated With Another Mental Disorder (Catatonia Specifier)', 'Catatonic Disorder Due to Another Medical Condition', 'Unspecified Catatonia', 'Other Specified Schizophrenia Spectrum and Other Psychotic Disorder', 'Unspecified Schizophrenia Spectrum and Other Psychotic Disorder', 'Bipolar I Disorder', 'Bipolar II Disorder', 'Cyclothymic Disorder', 'Substance/Medication-Induced Bipolar and Related Disorder', 'Bipolar and Related Disorder Due to Another Medical Condition', 'Other Specified Bipolar and Related Disorder', 'Unspecified Bipolar and Related Disorder', 'Disruptive Mood Dysregulation Disorder', 'Major Depressive Disorder, Single and Recurrent Episodes', 'Persistent Depressive Disorder (Dysthymia)', 'Premenstrual Dysphoric Disorder', 'Substance/Medication-Induced Depressive Disorder', 'Depressive Disorder Due to Another Medical Condition', 'Other Specified Depressive Disorder', 'Unspecified Depressive Disorder', 'Separation Anxiety Disorder', 'Selective Mutism', 'Specific Phobia', 'Social Anxiety Disorder (Social Phobia)', 'Panic Disorder', 'Panic Attack (Specifier)', 'Agoraphobia', 'Generalized Anxiety Disorder', 'Substance/Medication-Induced Anxiety Disorder', 'Anxiety Disorder Due to Another Medical Condition', 'Other Specified Anxiety Disorder', 'Unspecified Anxiety Disorder', 'Obsessive-Compulsive Disorder', 'Body Dysmorphic Disorder', 'Hoarding Disorder', 'Trichotillomania (Hair-Pulling Disorder)', 'Excoriation (Skin-Picking) Disorder', 'Substance/Medication-Induced Obsessive-Compulsive and Related Disorder', 'Obsessive-Compulsive and Related Disorder Due to Another Medical Condition', 'Other Specified Obsessive-Compulsive and Related Disorder', 'Unspecified Obsessive-Compulsive and Related Disorder', 'Reactive Attachment Disorder', 'Disinhibited Social Engagement Disorder', 'Posttraumatic Stress Disorder', 'Acute Stress Disorder', 'Adjustment Disorders', 'Other Specified Trauma- and Stressor-Related Disorder', 'Unspecified Trauma- and Stressor-Related Disorder', 'Dissociative Identity Disorder', 'Dissociative Amnesia', 'Depersonalization/Derealization Disorder', 'Other Specified Dissociative Disorder', 'Unspecified Dissociative Disorder', 'Somatic Symptom Disorder', 'Illness Anxiety Disorder', 'Conversion Disorder (Functional Neurological Symptom Disorder)', 'Psychological Factors Affecting Other Medical Conditions', 'Factitious Disorder', 'Other Specified Somatic Symptom and Related Disorder', 'Unspecified Somatic Symptom and Related Disorder', 'Pica', 'Rumination Disorder', 'Avoidant/Restrictive Food Intake Disorder', 'Anorexia Nervosa', 'Bulimia Nervosa', 'Binge-Eating Disorder', 'Other Specified Feeding or Eating Disorder', 'Unspecified Feeding or Eating Disorder', 'Enuresis', 'Encopresis', 'Other Specified Elimination Disorder', 'Unspecified Elimination Disorder', 'Insomnia Disorder', 'Hypersomnolence Disorder', 'Narcolepsy', 'Obstructive Sleep Apnea Hypopnea', 'Central Sleep Apnea', 'Sleep-Related Hypoventilation', 'Circadian Rhythm Sleep-Wake Disorders', 'Non–Rapid Eye Movement Sleep Arousal Disorders', 'Sleepwalking', 'Sleep Terrors', 'Nightmare Disorder', 'Rapid Eye Movement Sleep Behavior Disorder', 'Restless Legs Syndrome', 'Substance/Medication-Induced Sleep Disorder', 'Other Specified Insomnia Disorder', 'Unspecified Insomnia Disorder', 'Other Specified Hypersomnolence Disorder', 'Unspecified Hypersomnolence Disorder', 'Other Specified Sleep-Wake Disorder', 'Unspecified Sleep-Wake Disorder', 'Delayed Ejaculation', 'Erectile Disorder', 'Female Orgasmic Disorder', 'Female Sexual Interest/Arousal Disorder', 'Genito-Pelvic Pain/Penetration Disorder', 'Male Hypoactive Sexual Desire Disorder', 'Premature (Early) Ejaculation', 'Substance/Medication-Induced Sexual Dysfunction', 'Other Specified Sexual Dysfunction', 'Unspecified Sexual Dysfunction', 'Gender Dysphoria', 'Other Specified Gender Dysphoria', 'Unspecified Gender Dysphoria', 'Oppositional Defiant Disorder', 'Intermittent Explosive Disorder', 'Conduct Disorder', 'Antisocial Personality Disorder', 'Pyromania', 'Kleptomania', 'Other Specified Disruptive, Impulse-Control, and Conduct Disorder' 'Unspecified Disruptive, Impulse-Control, and Conduct Disorder', 'Substance Use Disorders', 'Substance-Induced Disorders', 'Substance Intoxication and Withdrawal' 'Substance/Medication-Induced Mental Disorders', 'Alcohol Use Disorder', 'Alcohol Intoxication', 'Alcohol Withdrawal', 'Other Alcohol-Induced Disorders', 'Unspecified Alcohol-Related Disorder', 'Caffeine Intoxication', 'Caffeine Withdrawal', 'Other Caffeine-Induced Disorders', 'Unspecified Caffeine-Related Disorder', 'Cannabis Use Disorder', 'Cannabis Intoxication', 'Cannabis Withdrawal', 'Other Cannabis-Induced Disorders', 'Unspecified Cannabis-Related Disorder', 'Phencyclidine Use Disorder', 'Other Hallucinogen Use Disorder', 'Phencyclidine Intoxication', 'Other Hallucinogen Intoxication', 'Hallucinogen Persisting Perception Disorder', 'Other Phencyclidine-Induced Disorders', 'Other Hallucinogen-Induced Disorders', 'Unspecified Phencyclidine-Related Disorder', 'Unspecified Hallucinogen-Related Disorder', 'Inhalant Use Disorder', 'Inhalant Intoxication', 'Other Inhalant-Induced Disorders', 'Unspecified Inhalant-Related Disorder', 'Opioid Use Disorder', 'Opioid Intoxication', 'Opioid Withdrawal', 'Other Opioid-Induced Disorders', 'Unspecified Opioid-Related Disorder', 'Sedative, Hypnotic, or Anxiolytic Use Disorder', 'Sedative, Hypnotic, or Anxiolytic Intoxication', 'Sedative, Hypnotic, or Anxiolytic Withdrawal', 'Other Sedative-, Hypnotic-, or Anxiolytic-Induced Disorders', 'Unspecified Sedative-, Hypnotic-, or Anxiolytic-Related Disorder', 'Stimulant Use Disorder', 'Stimulant Intoxication', 'Stimulant Withdrawal', 'Other Stimulant-Induced Disorders', 'Unspecified Stimulant-Related Disorder', 'Tobacco Use Disorder', 'Tobacco Withdrawal', 'Other Tobacco-Induced Disorders', 'Unspecified Tobacco-Related Disorder', 'Other (or Unknown) Substance Use Disorder', 'Other (or Unknown) Substance Intoxication', 'Other (or Unknown) Substance Withdrawal', 'Other (or Unknown) Substance–Induced Disorders', 'Unspecified Other (or Unknown) Substance–Related Disorder', 'Gambling Disorder', 'Delirium', 'Other Specified Delirium', 'Unspecified Delirium', 'Major Neurocognitive Disorder', 'Mild Neurocognitive Disorder', 'Major or Mild Neurocognitive Disorder Due to Alzheimer’s Disease', 'Major or Mild Frontotemporal Neurocognitive Disorder', 'Major or Mild Neurocognitive Disorder With Lewy Bodies', 'Major or Mild Vascular Neurocognitive Disorder', 'Major or Mild Neurocognitive Disorder Due to Traumatic Brain Injury', 'Substance/Medication-Induced Major or Mild Neurocognitive Disorder', 'Major or Mild Neurocognitive Disorder Due to HIV Infection', 'Major or Mild Neurocognitive Disorder Due to Prion Disease', 'Major or Mild Neurocognitive Disorder Due to Parkinson’s Disease', 'Major or Mild Neurocognitive Disorder Due to Huntington’s Disease', 'Major or Mild Neurocognitive Disorder Due to Another Medical Condition', 'Major or Mild Neurocognitive Disorder Due to Multiple Etiologies', 'Unspecified Neurocognitive Disorder', 'General Personality Disorder', 'Paranoid Personality Disorder', 'Schizoid Personality Disorder', 'Schizotypal Personality Disorder', 'Antisocial Personality Disorder', 'Borderline Personality Disorder', 'Histrionic Personality Disorder', 'Narcissistic Personality Disorder', 'Avoidant Personality Disorder', 'Dependent Personality Disorder', 'Obsessive-Compulsive Personality Disorder', 'Personality Change Due to Another Medical Condition', 'Other Specified Personality Disorder', 'Unspecified Personality Disorder', 'Voyeuristic Disorder', 'Exhibitionistic Disorder', 'Frotteuristic Disorder', 'Sexual Masochism Disorder', 'Sexual Sadism Disorder', 'Pedophilic Disorder', 'Fetishistic Disorder', 'Transvestic Disorder', 'Other Specified Paraphilic Disorder', 'Unspecified Paraphilic Disorder', 'Other Specified Mental Disorder Due to Another Medical Condition', 'Unspecified Mental Disorder Due to Another Medical Condition', 'Other Specified Mental Disorder', 'Unspecified Mental Disorder'}

            # chain 1
            template = """You are a pathological psychology teacher. Given a disorder input, your job is to generate a paragraph of case study for the disorder \
                        which would include, either all or not, the diagnosis criterias from DSM-V for your student as an exam. Please also include the client's alias and age \
                        (also randomise this). But please do not include the answer (the disorder name) so you can test your students. DO NOT ANALYSE WHICH DISORDER THE CLIENT \
                        HAVE YET. THIS IS AN EXAM SO DO NOT DARE TO WRITE ANY DISORDER NAME OR THE CRITERIAS AS A CLUE OR AS AN ANSWER.

                        disorder: {input}
                        """
            dis_chat = ChatOpenAI(temperature=0.5, model=llm_model)
            disorder_prompt_template = PromptTemplate(input_variables=["input"], template=template)
            disorder_chain = LLMChain(llm=dis_chat, prompt=disorder_prompt_template, output_key="case")

            # chain 2
            analys_template = """You are a psychological pathology teacher. Given the case study, your job is to analyse \
                                the case and extract the following information: the client's alias, age, symptoms and possible disorders \
                                according to DSM-V.

                                You should list every possible disorder that the symptoms match the criterias in DSM-V. In each disorder, list all the criterias in DSM-V. \
                                After each criteria, include the client's symptoms that match the criteria in a parenthesis, separated by a comma. If there aren't any \
                                symptoms to match, return 'no info'.

                                Case: {case}
                                """
            ana_chat = ChatOpenAI(temperature=0.0, model=llm_model)
            analys_prompt_template = PromptTemplate(input_variables=["case"], template=analys_template)
            analys_chain = LLMChain(llm=ana_chat, prompt=analys_prompt_template, output_key="analysis")

            overall_chain = SequentialChain(
                chains=[disorder_chain, analys_chain],
                input_variables=["input"],
                output_variables=["case", "analysis"],
                verbose=True)
            
            disorder = random.choice(list(disorder_set))
            result = overall_chain({"input": disorder})

            st.write(result['case'])
            st.write(result['analysis'])
        except Exception as e:
            st.write(f'An error occured: {e}')

st.balloons()