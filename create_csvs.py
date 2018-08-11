import csv
import pandas as pd
import numpy as np

base_csv = "uiuc-gpa-dataset.csv"
grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'W']

def main():
    fix_base_csv()
    process_csv_data()

#TODO Add info to fix here
def fix_base_csv():
    base = pd.read_csv(base_csv)
    base['Course_Title'] = base['Course_Title'].str.replace(' & ', ' and ')
    base['Course_Title'] = base['Course_Title'].str.replace('Orgnizations', 'Organizations')
    base['Course_Title'] = base['Course_Title'].str.replace('Anlaytics', 'Analytics')
    base['Course_Title'] = base['Course_Title'].str.replace('CAD', 'Computer-Aided Design')
    base['Course_Title'] = base['Course_Title'].str.replace('Computer Aided', 'Computer-Aided')
    base = base.to_csv('test.csv', index=False)

def process_csv_data():
    avg_gpa_params = ['Subject', 'Number', 'Course_Title']
    create_csv('avg-gpa-dataset.csv', avg_gpa_params, 'avg_gpa')

    prof_avg_params = ['Subject', 'Number', 'Course_Title', 'Primary_Instructor']
    create_csv('prof-gpa-dataset.csv', prof_avg_params, 'avg_prof_gpa')

def create_csv(csv_name, params, new_avg_name):
    prep_csvs(csv_name)
    new_csv = pd.read_csv(csv_name)

    new_csv = new_csv.groupby(params)[grades].sum()

    total_points = points_from_grades(new_csv)
    total_students = pop_from_grades(new_csv)
    new_avg_value = total_points / total_students
    new_csv[new_avg_name] = np.round(new_avg_value, 2)

    new_csv = new_csv.to_csv(csv_name)

def prep_csvs(csv_name):
    with open(base_csv, "r") as source:
        rdr = csv.reader(source)
        with open(csv_name, "w") as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow((r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10],
                r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20]))

def points_from_grades(csv):
    return (4.00*csv['A+'] + 4.00*csv['A'] + (3+2/3)*csv['A-']
            + (3+1/3)*csv['B+'] + 3.00*csv['B'] + (2+2/3)*csv['B-']
            + (2+1/3)*csv['C+'] + 2.00*csv['C'] + (1+2/3)*csv['C-']
            + (1+1/3)*csv['D+'] + 1.00*csv['D'] + (2/3)*csv['D-'])

#TODO Check if 'W' grades should be included
def pop_from_grades(csv):
    return (csv['A+'] + csv['A'] + csv['A-'] + csv['B+'] + csv['B'] + csv['B-']
            + csv['C+'] + csv['C'] + csv['C-'] + csv['D+']+ csv['D'] + csv['D-']
            + csv['F'] + csv['W'])

if __name__ == "__main__":
    main()
