import requests
from urllib.parse import unquote
from pycomcigan import TimeTable, get_school_code

def string_to_binary(input_string):
    # 문자열을 바이트로 인코딩
    byte_array = input_string.encode()
    
    # 각 바이트를 8자리 이진수로 변환하여 리스트에 저장
    binary_list = [format(byte, '08b') for byte in byte_array]
    
    # 이진수 리스트를 하나의 문자열로 합침
    binary_string = ''.join(binary_list)
    
    # 바이트 문자열로 변환
    binary_bytes = b''.join(bytes([int(binary_list[i], 2)]) for i in range(len(binary_list)))
    
    return binary_bytes

def get_school(school:str):
    '''
    가장 비슷한 이름의 학교 리스트를 반환함
    '''
    url = f'https://open.neis.go.kr/hub/schoolInfo?Type=json&SCHUL_NM={school}'

    # GET 요청을 보내고 응답을 받음
    response = requests.get(url)

    # 응답이 성공적이면 JSON 데이터를 추출
    if response.status_code == 200:
        data = response.json()

        # 학교 이름을 추출
        school_names = []

        # JSON 데이터에서 학교 이름 추출
        for item in data.get('schoolInfo', [])[1].get('row', []):
            school_name = item.get('SCHUL_NM', '')
            if school_name:
                school_names.append(school_name)

        # 학교 이름 리스트를 출력
        return {"success": True, "school_names": school_names}
    else:
        return {"success": False, "error": response.text}

def get_comci_school_code(school:str):
    '''
    가장 비슷한 이름의 컴시간 학교 코드를 반환함
    '''
    return get_school_code(school)

def get_timetable(school: str, grade: int, cls: int, next_week: bool):
    school = unquote(school)
    try:
        timetable = TimeTable(school, week_num=1 if next_week else 0)
    except RuntimeError as e:
        return {"success": False, "error": str(e)}
    except IndexError as e:
        return {"success": False, "error": str(e)}
    
    timetable = TimeTable(school, week_num=1 if next_week else 0)

    parsing = {"success": True}
    
    for day in range(1, 6):
        # Initialize nested dictionaries if they don't exist
        if grade not in parsing:
            parsing[grade] = {}
        if cls not in parsing[grade]:
            parsing[grade][cls] = {}
        if day not in parsing[grade][cls]:
            parsing[grade][cls][day] = {}
        if "time" not in parsing[grade][cls][day]:
            parsing[grade][cls][day] = {}
        
        for time in range(len(timetable.timetable[grade][cls][day])):
            split_text = str(timetable.timetable[grade][cls][day][time]).split()
            
            # Initialize time dictionary if it doesn't exist
            if time not in parsing[grade][cls][day]:
                parsing[grade][cls][day][time] = {}
            
            s = split_text[1].split("(")
            try:
                parsing[grade][cls][day][time]["subject"] = s[0]
                parsing[grade][cls][day][time]["teacher"] = s[1].replace(")", "")
            except IndexError as e:
                return {"success": True, "error": e, "value": s}

            try:
                parsing[grade][cls][day][time]["change"] = False if split_text[2] is None else True
            except IndexError:
                parsing[grade][cls][day][time]["change"] = False

    return parsing