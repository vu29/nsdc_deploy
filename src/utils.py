import pandas as pd
import pickle
import json


def format_dict(input_dict):
    name_correction_dict = {
        'Age Group': 'agegroup',
        'Caste Category': 'castecategory',
        'Type of Disability': 'TypeofDisability'

    }
    new_dict = dict()
    for key in input_dict.keys():
        if key in name_correction_dict:
            new_key = name_correction_dict[key]
            new_dict[new_key] = int(input_dict[key])
        else:
            new_dict[key] = int(input_dict[key])
    return new_dict


def get_prediction_without_result(form_data,):
    final_col_order = ['Gender', 'TypeofDisability', 'castecategory', 'Religion', 'JobRole', 'SectorName', 'PartnerName', 'TC State', 'TC District', 'TC Name', 'TotalCandidatesinBatch', 'agegroup', 'EducationLevel','No. of colleges', 'Trade Count', 'No of ITI', 'Ph.D', 'M.Phil', 'Post Graduate', 'Under Graduate', 'PG Diploma', 'Diploma', 'Certificate', 'Integrated', 'Total Number of Schools', 'Total Poulation', 'Sexratio', 'Decadal Growth Rate', 'Overall Literacy', 'Female Literacy', 'Primary Enrollment', 'Primary with Upper Primary Enrollment', 'Primary with Upper Primary sec/higher sec. Enrollment', 'Upper Primary Only Enrollment', 'Upper Primary with sec./higher sec. Enrollment', 'Primary Teacher', 'Primary with Upper Primary Teacher', 'Primary with Upper Primary sec/higher sec. Teacher', 'Upper Primary Only Teacher', 'Upper Primary with sec./higher sec. Teacher', 'number of Industry total', 'Business Services', 'Manufacturing (Food stuffs)', 'Real Estate and Renting', 'Trading', 'Community, personal & Social Services', 'Agriculture and Allied Activities', 'Construction', 'Manufacturing (Textiles)', 'Transport, storage and Communications', 'Electricity, Gas & Water companies', 'Manufacturing (Paper & Paper products, Publishing, printing and reproduction of recorded media)', 'Manufacturing (Machinery & Equipments)', 'Manufacturing (Others)', 'Finance', 'Manufacturing (Metals & Chemicals, and products thereof)', 'Manufacturing (Leather & products thereof)', 'Mining & Quarrying', 'Manufacturing (Wood Products)', 'Insurance', 'Manufacturing (Paper & Paper products, Publishing, PRIVnting and reproduction of recorded media)', 'Total population', 'Population Age(15-21)', 'Population (15-24) Absolute', 'Population (5-14) Absolute', 'Population Total male', 'Population Total female', 'Population Hindu', 'Population Muslim', 'Population christian', 'Population Sikh', 'Population Jain', 'Population other', 'Total Households', 'Total Rural Household', 'Total Urban Household', 'Number Normal Rural', 'Number Normal Urban', 'Institutional Rural', 'Institutional Urban', 'Houseless Rural', 'Houseless Urban', 'Houseless with Shelter Urban', 'Houseless without Shelter Urban', 'Total Population', 'No of Population Having Highest Education Level of Illitrate', 'No of Population Having Highest Education Level of Llitrate But Below Primary', 'No of Population Having Highest Education Level of Primary', 'No of Population Having Highest Education Level of Middle', 'No of Population Having Highest Education Level of Secondary', 'No of Population Having Highest Education Level of Higher Secondary', 'No of Population Having Highest Education Level of Graduate Or Higher', 'Not In Labour Force', 'Employed', 'Unemployed']
    form_data = format_dict(form_data)
    dist_code = form_data['TC District']
    state_dict = json.load(open('./models/final_data/dist_state_code.json'))
    state_code = state_dict[str(dist_code)]
    df = pd.DataFrame.from_dict(json.load(
        open('./models/final_data/tc_sector_partner_jobrole_with_code.json'))[str(dist_code)])
    df['TC District'] = int(dist_code)
    df['TC State'] = int(state_code)
    for col in form_data:
        df[col] = form_data[col]
    dist_df = pd.read_csv('./models/final_data/final_dist_normalized.csv')
    dist_df = dist_df[dist_df['District'] == dist_code].iloc[:, 1:]
    dist_values = dist_df.iloc[0, :].items()
    for key, value in dist_values:
        df[key] = value
    X = df[final_col_order].values
    print(X)
    model = pickle.load(open('./models/model_withoutresult_external.sav', 'rb'))
    prediction = model.predict(X).tolist()
    table_df = df[['TC Name','PartnerName','SectorName','JobRole']]
    nsdc_json = json.load(open('./models/final_data/dictnsdc.json','r'))
    for col in table_df.columns:
        current_dict = dict(zip(nsdc_json[col].values(),nsdc_json[col].keys()))
        table_df[col] = table_df[col].map(lambda x : current_dict[x])
    data = table_df.to_dict('row')
    for i in range(len(prediction)):
        data[i]['Result'] = prediction[i]
    return data


def get_prediction_with_result(form_data):
    final_col_order = ['Gender', 'TypeofDisability', 'castecategory', 'Religion', 'JobRole', 'SectorName', 'PartnerName', 'TC State', 'TC District', 'TC Name', 'TotalCandidatesinBatch', 'Result', 'Grade', 'Certified', 'agegroup', 'EducationLevel','No. of colleges', 'Trade Count', 'No of ITI', 'Ph.D', 'M.Phil', 'Post Graduate', 'Under Graduate', 'PG Diploma', 'Diploma', 'Certificate', 'Integrated', 'Total Number of Schools', 'Total Poulation', 'Sexratio', 'Decadal Growth Rate', 'Overall Literacy', 'Female Literacy', 'Primary Enrollment', 'Primary with Upper Primary Enrollment', 'Primary with Upper Primary sec/higher sec. Enrollment', 'Upper Primary Only Enrollment', 'Upper Primary with sec./higher sec. Enrollment', 'Primary Teacher', 'Primary with Upper Primary Teacher', 'Primary with Upper Primary sec/higher sec. Teacher', 'Upper Primary Only Teacher', 'Upper Primary with sec./higher sec. Teacher', 'number of Industry total', 'Business Services', 'Manufacturing (Food stuffs)', 'Real Estate and Renting', 'Trading', 'Community, personal & Social Services', 'Agriculture and Allied Activities', 'Construction', 'Manufacturing (Textiles)', 'Transport, storage and Communications', 'Electricity, Gas & Water companies', 'Manufacturing (Paper & Paper products, Publishing, printing and reproduction of recorded media)', 'Manufacturing (Machinery & Equipments)', 'Manufacturing (Others)', 'Finance', 'Manufacturing (Metals & Chemicals, and products thereof)', 'Manufacturing (Leather & products thereof)', 'Mining & Quarrying', 'Manufacturing (Wood Products)', 'Insurance', 'Manufacturing (Paper & Paper products, Publishing, PRIVnting and reproduction of recorded media)', 'Total population', 'Population Age(15-21)', 'Population (15-24) Absolute', 'Population (5-14) Absolute', 'Population Total male', 'Population Total female', 'Population Hindu', 'Population Muslim', 'Population christian', 'Population Sikh', 'Population Jain', 'Population other', 'Total Households', 'Total Rural Household', 'Total Urban Household', 'Number Normal Rural', 'Number Normal Urban', 'Institutional Rural', 'Institutional Urban', 'Houseless Rural', 'Houseless Urban', 'Houseless with Shelter Urban', 'Houseless without Shelter Urban', 'Total Population', 'No of Population Having Highest Education Level of Illitrate', 'No of Population Having Highest Education Level of Llitrate But Below Primary', 'No of Population Having Highest Education Level of Primary', 'No of Population Having Highest Education Level of Middle', 'No of Population Having Highest Education Level of Secondary', 'No of Population Having Highest Education Level of Higher Secondary', 'No of Population Having Highest Education Level of Graduate Or Higher', 'Not In Labour Force', 'Employed', 'Unemployed']
    form_data = format_dict(form_data)
    dist_code = form_data['TC District']
    state_dict = json.load(open('./models/final_data/dist_state_code.json'))
    state_code = state_dict[str(dist_code)]
    df = pd.DataFrame.from_dict(json.load(
        open('./models/final_data/tc_sector_partner_jobrole_with_code.json'))[str(dist_code)])
    df['TC District'] = int(dist_code)
    df['TC State'] = int(state_code)
    for col in form_data:
        df[col] = form_data[col]
    dist_df = pd.read_csv('./models/final_data/final_dist_normalized.csv')
    dist_df = dist_df[dist_df['District'] == dist_code].iloc[:, 1:]
    dist_values = dist_df.iloc[0, :].items()
    for key, value in dist_values:
        df[key] = value
    X = df[final_col_order].values
    model = pickle.load(open('./models/model_withresult_external.sav', 'rb'))
    prediction = model.predict(X).tolist()
    table_df = df[['TC Name','PartnerName','SectorName','JobRole']]
    nsdc_json = json.load(open('./models/final_data/dictnsdc.json','r'))
    for col in table_df.columns:
        current_dict = dict(zip(nsdc_json[col].values(),nsdc_json[col].keys()))
        table_df[col] = table_df[col].map(lambda x : current_dict[x])
    data = table_df.to_dict('row')
    for i in range(len(prediction)):
        data[i]['Result'] = prediction[i]
    return data