import csv
import requests
import time
from time import strptime
import xml.etree.ElementTree as ET

year = 2018
term = "fall"
base_url = "http://courses.illinois.edu/cisapp/explorer/schedule/" + str(year) + "/" + term

#NOTE Exluded in the process was ['VM']
def main():
    create_csvs()

    subjects = []
    get_subjects(subjects)

    for sub in subjects:
        #NOTE: 'VM' excluded from dataset due to only having 600 level courses with large amount of instructors
        if sub == 'VM':
            continue

        print("Trying to Process Subject: " + sub)
        request = requests.get(base_url + "/" + sub + ".xml?mode=cascade")
        courses = ET.fromstring(request.content)

        for course in courses.iter('cascadingCourse'):
            course_info = []
            add_course_info(course, course_info)
            write_row_to_file('course_list.csv', course_info)

            for section in course.iter('detailedSection'):
                section_info = []
                section_info.extend(course_info)
                add_section_info(section, section_info)
                section_num = section.find('sectionNumber')

                if section_num is not None:
                    section_num = section_num.text
                    section_info.append(section_num)

                    for meeting in section.iter('meeting'):
                        meeting_info = []
                        meeting_info.extend(section_info)
                        start_time = meeting.find('start').text

                        if start_time == 'ARRANGED':
                            add_arranged_meeting_info(meeting, meeting_info)
                            add_instructor_info(meeting, meeting_info)
                            type_name = meeting.find('type').text

                            if type_name == 'Online':
                                write_row_to_file('online_courses.csv', meeting_info)
                            else:
                                write_row_to_file('arranged_courses.csv', meeting_info)
                        else:
                            room = meeting.find('roomNumber')
                            if room is not None:
                                add_all_meeting_info(meeting, meeting_info)
                                add_instructor_info(meeting, meeting_info)
                                write_row_to_file('course_meetings.csv', meeting_info)
                            else:
                                add_partial_meeting_info(meeting, meeting_info)
                                add_instructor_info(meeting, meeting_info)
                                write_row_to_file('no_location_courses.csv', meeting_info)
                else:
                    for meeting in section.iter('meeting'):
                        meeting_info = []
                        meeting_info.extend(section_info)
                        add_arranged_meeting_info(meeting, meeting_info)
                        write_row_to_file('independent_courses.csv', meeting_info)
        time.sleep(10)

def create_csvs():
    header = ['Course', 'Title', 'Credit_Hours']
    format_csvs('course_list.csv', header)

    header_ext = ['Status', 'Start_Date','End_Date', 'Type_Code', 'Type_Name', "Start_Time"]
    header.extend(header_ext)
    format_csvs('independent_courses.csv', header)

    instructor_ext = ['Inst1_Last', 'Inst1_First', 'Inst1_Full',
                        'Inst2_Last', 'Inst2_First', 'Inst2_Full',
                        'Inst3_Last', 'Inst3_First', 'Inst3_Full',
                        'Inst4_Last', 'Inst4_First', 'Inst4_Full',
                        'Inst5_Last', 'Inst5_First', 'Inst5_Full',
                        'Inst6_Last', 'Inst6_First', 'Inst6_Full',
                        'Inst7_Last', 'Inst7_First', 'Inst7_Full',
                        'Inst8_Last', 'Inst8_First', 'Inst8_Full',
                        'Inst9_Last', 'Inst9_First', 'Inst9_Full',
                        'Inst10_Last', 'Inst10_First', 'Inst10_Full',
                        'Inst11_Last', 'Inst11_First', 'Inst11_Full',
                        'Inst12_Last', 'Inst12_First', 'Inst12_Full']
    header2 = []
    header2.extend(header)
    header2.extend(instructor_ext)
    format_csvs('online_courses.csv', header2)
    format_csvs('arranged_courses.csv', header2)

    partial_ext = ['End_Time', 'Meeting_Days']
    header.extend(partial_ext)

    header2 = []
    header2.extend(header)
    header2.extend(instructor_ext)
    format_csvs('no_location_courses.csv', header2)

    full_ext = ['Room', 'Building']
    header.extend(full_ext)
    header.extend(instructor_ext)
    format_csvs('course_meetings.csv', header)

def format_csvs(csv_name, header):
    with open(csv_name, 'w') as file:
        fileWtr = csv.writer(file)
        fileWtr.writerow(header)

def write_row_to_file(csv_name, values):
    with open(csv_name, 'a') as file:
        fileWtr = csv.writer(file)
        fileWtr.writerow(values)

def get_subjects(subjects):
    request = requests.get(base_url + ".xml")
    root = ET.fromstring(request.content)

    for child in root.iter('subject'):
        subjects.append(child.attrib['id'])

    time.sleep(10)

def add_course_info(course, values):
    course_id = course.attrib['id']
    course_title = course.find('label').text
    credit_hours = course.find('creditHours').text

    values.append(course_id)
    values.append(course_title)
    values.append(credit_hours)

def add_section_info(section, values):
    sec_status = section.find('enrollmentStatus').text
    sec_dateRange = section.find('sectionDateRange')
    sec_start =  section.find('startDate')
    sec_end = ''

    if sec_start is not None:
        sec_start = sec_start.text
        sec_end = section.find('endDate').text
    elif sec_dateRange is not None:
        sec_dateRange = sec_dateRange.text
        month = strptime(sec_dateRange[9:12], '%b').tm_mon
        sec_start = '20' + sec_dateRange[13:15] + '-' + str(month).zfill(2) + '-' + sec_dateRange[6:9]  + "05:00"
        month = strptime(sec_dateRange[21:24], '%b').tm_mon
        sec_end = '20' + sec_dateRange[25:27] + '-' + str(month).zfill(2) + '-' + sec_dateRange[18:21]  + "06:00"
    else:
        #TODO Remember to parse these out in the files
        sec_start = 'Unspecfied'
        sec_end = 'Unspecfied'
        print("Unspecfied Section")

    values.append(sec_status)
    values.append(sec_start)
    values.append(sec_end)

def add_arranged_meeting_info(meeting, values):
    type = meeting.find('type')
    type_code = type.attrib['code']
    type_name = type.text
    start_time = meeting.find('start').text

    values.append(type_code)
    values.append(type_name)
    values.append(start_time)

def add_partial_meeting_info(meeting, values):
    add_arranged_meeting_info(meeting, values)

    end_time = meeting.find('end').text
    meeting_days = meeting.find('daysOfTheWeek')

    if meeting_days is not None:
        meeting_days = meeting_days.text
    else:
        #TODO Remember to parse these out in the files
        meeting_days = "Unspecfied"
        print("Unspecfied Meeting_Days")

    values.append(end_time)
    values.append(meeting_days)

def add_all_meeting_info(meeting, values):
    add_partial_meeting_info(meeting, values)

    room = meeting.find('roomNumber').text
    building = meeting.find('buildingName').text

    values.append(room)
    values.append(building)

#TODO There is a large amount of extraneous instructors, easier to parse out later
def add_instructor_info(meeting, values):
    count = 0

    for instructor in meeting.iter('instructor'):
        instructor_lastName = instructor.attrib['lastName']
        instructor_firstName = instructor.attrib['firstName']
        instructor_fullName = instructor.text
        values.append(instructor_lastName)
        values.append(instructor_firstName)
        values.append(instructor_fullName)
        count += 1

    if count < 12:
        for i in range(count, 12):
            values.append('None')
            values.append('None')
            values.append('None')
    elif count > 12:
        print("Instructor Problem with Actual Count:" + str(count))

if __name__ == "__main__":
    main()
