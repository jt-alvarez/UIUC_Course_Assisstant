import csv
import pandas as pd
import numpy as np

def main():
    process_csv_data()

def process_csv_data():
    with open("uiuc-gpa-dataset.csv", "r") as source:
        rdr = csv.reader(source)
        with open("avg-gpa-dataset.csv", "w") as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow((r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10],
                r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19]))

    class_avg = pd.read_csv("avg-gpa-dataset.csv")
    class_avg = class_avg.groupby(['Subject', 'Number', 'Course_Title'])['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'W'].sum()

    value = (4.00*class_avg['A+'] + 4.00*class_avg['A'] + (3+2/3)*class_avg['A-']
            + (3+1/3)*class_avg['B+'] + 3.00*class_avg['B'] + (2+2/3)*class_avg['B-']
            + (2+1/3)*class_avg['C+'] + 2.00*class_avg['C'] + (1+2/3)*class_avg['C-']
            + (1+1/3)*class_avg['D+'] + 1.00*class_avg['D'] + (2/3)*class_avg['D-'])/(
            class_avg['A+'] + class_avg['A'] + class_avg['A-'] + class_avg['B+']
            + class_avg['B'] + class_avg['B-'] + class_avg['C+'] + class_avg['C']
            + class_avg['C-'] + class_avg['D+']+ class_avg['D'] + class_avg['D-']
            + class_avg['F'] + class_avg['W'])

    class_avg['avg_gpa'] = np.round(value, 2)
    class_avg = class_avg.to_csv("avg-gpa-dataset.csv")

    with open("uiuc-gpa-dataset.csv", "r") as source:
        rdr = csv.reader(source)
        with open("prof-gpa-dataset.csv", "w") as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow((r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10],
                r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20]))

    prof_avg = pd.read_csv("prof-gpa-dataset.csv")
    prof_avg = prof_avg.groupby(['Subject', 'Number', 'Course_Title', 'Primary_Instructor'])['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'W'].sum()

    value = (4.00*prof_avg['A+'] + 4.00*prof_avg['A'] + 3.67*prof_avg['A-']
            + 3.33*prof_avg['B+'] + 3.00*prof_avg['B'] + 2.67*prof_avg['B-']
            + 2.33*prof_avg['C+'] + 2.00*prof_avg['C'] + 1.67*prof_avg['C-']
            + 1.33*prof_avg['D+'] + 1.00*prof_avg['D'] + 0.67*prof_avg['D-']
            + 0.00*prof_avg['F']) / (prof_avg['A+'] + prof_avg['A'] + prof_avg['A-']
            + prof_avg['B+'] + prof_avg['B'] + prof_avg['B-'] + prof_avg['C+']
            + prof_avg['C'] + prof_avg['C-'] + prof_avg['D+']+ prof_avg['D']
            + prof_avg['D-'] + prof_avg['F'] + prof_avg['W'])

    prof_avg['avg_prof_gpa'] = np.round(value, 2)
    prof_avg = prof_avg.to_csv("prof-gpa-dataset.csv")

if __name__ == "__main__":
    main()
