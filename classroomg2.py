import cv2
from PIL import Image
import numpy as np
import random
import csv

classroom_path = r'C:\Users\dell\Desktop\classroom\360_F_787478668_mNfiOcUF3nEMunjEGceuZVbEwUv3abYS.jpg'
classroom = cv2.imread(classroom_path)

if classroom is None:
    raise FileNotFoundError(f"Could not load the classroom image from the path: {classroom_path}")

classroom = cv2.resize(classroom, (3850, 2160))

def place_person_in_classroom(classroom, person_image_path, position):
    try:
        person = Image.open(person_image_path).convert("RGBA")
        person = person.resize((120, 200))
        classroom_pil = Image.fromarray(cv2.cvtColor(classroom, cv2.COLOR_BGR2RGB)).convert("RGBA")
        classroom_pil.paste(person, position, person)
        classroom = cv2.cvtColor(np.array(classroom_pil), cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        print(f"Error: Could not load person image from {person_image_path}. Skipping this person.")
    return classroom

def generate_classroom_with_people(classroom, people_image_paths, positions, image_number):
    random.shuffle(people_image_paths)
    num_students = min(len(positions), 15)
    selected_people_images = people_image_paths[:num_students]
    
    csv_data = []
    for idx, pos in enumerate(positions[:num_students]):
        person_image_path = selected_people_images[idx]
        classroom = place_person_in_classroom(classroom, person_image_path, pos)
        student_image_name = person_image_path.split('\\')[-1]
        csv_data.append([student_image_name, pos])
    
    output_image_path = f'C:\\Users\\dell\\Desktop\\classroom\\classroom_with_{image_number}_students.png'
    cv2.imwrite(output_image_path, classroom)
    print(f"Classroom image with {num_students} students saved at {output_image_path}")

    csv_output_path = f'C:\\Users\\dell\\Desktop\\classroom\\classroom_students_info_{image_number}.csv'
    with open(csv_output_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Student Image', 'Position'])
        csv_writer.writerows(csv_data)
    print(f"CSV file saved at {csv_output_path}")

positions = [
    (500, 1100), (1200, 1100), (1800, 1100), (2400, 1100), (2800, 1100),
    (800, 1100), (3100, 1100), (300, 1200), (1000, 1200), (2600, 1200),
    (3300, 1200), (90, 1300), (750, 1300), (2800, 1300), (3700, 1300)
]

people_image_paths = [
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\02_AAQUIB HANAN.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\01_Aaliya M Ismail.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\04_Abhijith AK.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\06_ABINAND B ARJUN.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\07_AFNA V N_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\08_Akshay S.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\09_Alan Benny_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\12_Anal Reji_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\14_Arjun S.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\15_Arrchitha Kesavadas_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\16_Arun Nand B S.JPG',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\17_Arya Ajayan.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\18_Arya N V.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\20_Aslam ks.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\21_Bharath S.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\22_Christina Dixon_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\24_Devika Padmanabhan.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\26_Gowri Sankara Kanth S.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\28_JOFIN JOJI.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\29_Jovita Joy.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\30_JOYAL JOSE.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\32_K Vaishnav Nair.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\33_Keerthana R Warrier.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\34_KRISHNAJA T N.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\35_Lakshmi A Nair.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\36_Lakshmi Balan.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\37_Lakshmi PM_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\38_M S Arjun.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\39_Maheswar Babu.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\40_MAHMOOD SHEFIN.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\44_Merin Johny_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\45_Merin philip .jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\46_Muhammed Fayiz M.A.jpeg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\53_NOGIL BINU_.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\54_Rapheal Rodic Sebastian .jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\56_SAMJISH.K.S.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\57_Sanal T.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\58_Sayaan Seemon.JPG',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\59_Sayandhana KS.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\60_SEBASTIAN SAJU P .jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\61_TOM SAIN.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\63_Varun Solaman.jpg',
    r'C:\Users\dell\Desktop\classroom\PHOTO_ID CARD\65_Zain Bastin.JPG'
]

# Run the generation process 20 times
for i in range(1, 21):
    generate_classroom_with_people(classroom.copy(), people_image_paths, positions, i)
