# step 1: user will upload an image and store it in firebase with a URL file name (OMRCamera.tsx)
# step 2: user will send a request to the backend to process the image (OMRCamera.tsx)
# step 3: backend will download the URL image and process it (app.py)
# step 4: backend will return the score to the localhost named http://127.0.0.1:5000/process_omr (app.py)
# step 5: frontend will fetch the score from the same localhost (OMRCamera.tsx)
# step 6: frontend will display the score (OMRCamera.tsx)



from io import BytesIO
import requests
import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def omr_processing(image):
    # Resize image if needed (adjust size based on your sheet size)
    image = cv2.resize(image, (1000, 1400))  # Adjust size as per your sheet
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold to make the paper white and answers black
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Define the grid positions for the answer bubbles
    answer_bubbles = {
        1: [(253, 182), (283, 182), (313, 182), (342, 182), (371, 182), (400, 182) ], 
        2: [(253, 212), (283, 212), (313, 212), (342, 212), (371, 212), (400, 212) ],
        3: [(253, 240), (283, 240), (313, 240), (342, 240), (371, 240), (400, 240) ],
        4: [(253, 270), (283, 270), (313, 270), (342, 270), (371, 270), (400, 270) ],
        5: [(254, 297), (283, 297), (313, 297), (342, 297), (371, 297), (400, 297) ],
        6: [(255, 327), (284, 327), (314, 327), (343, 327), (372, 327), (401, 327) ],
        7: [(254, 357), (283, 357), (313, 357), (342, 357), (371, 357), (400, 357) ],
        8: [(255, 387), (284, 387), (314, 387), (343, 387), (372, 387), (401, 387) ],
        9: [(255, 415), (284, 415), (314, 415), (343, 415), (372, 415), (401, 415) ],
        10: [(255, 444), (284, 444), (314, 444), (343, 444), (372, 444), (401, 444) ],
        11: [(255, 471), (284, 471), (314, 471), (343, 471), (372, 471), (401, 471) ],
        12: [(255, 501), (284, 501), (314, 501), (343, 501), (372, 501), (401, 501) ],

        13: [(614, 185), (644, 185), (674, 185), (702, 185), (732, 185), (760, 185) ],
        14: [(615, 214), (645, 214), (674, 214), (703, 214), (732, 214), (761, 214) ],
        15: [(614, 242), (644, 242), (674, 242), (702, 242), (732, 242), (760, 242) ],
        16: [(615, 272), (645, 272), (675, 272), (703, 272), (733, 272), (761, 272) ],
        17: [(616, 299), (646, 299), (676, 299), (704, 299), (734, 299), (762, 299) ],
        18: [(616, 330), (646, 330), (676, 330), (704, 330), (734, 330), (762, 330) ],
        19: [(616, 359), (646, 359), (676, 359), (704, 359), (734, 359), (762, 359) ],
        20: [(616, 389), (646, 389), (676, 389), (704, 389), (734, 389), (762, 389) ],
        21: [(616, 416), (646, 416), (676, 416), (704, 416), (734, 416), (762, 416) ],
        22: [(616, 446), (646, 446), (676, 446), (704, 446), (734, 446), (762, 446) ],
        23: [(616, 473), (646, 473), (676, 473), (704, 473), (734, 473), (762, 473) ],
        24: [(616, 503), (646, 503), (676, 503), (704, 503), (734, 503), (762, 503) ],

        25: [(105, 745), (136, 745), (164, 745), (193, 745) , (222, 745), (250, 745), (280, 745) , (308, 745)],
        26: [(105, 771), (136, 772), (164, 772) , (193, 772), (222, 772), (252, 772), (280, 772) , (308, 772)],
        27: [(105, 798), (136, 798), (164, 798) , (194, 798), (222, 798), (252, 798), (280, 798) , (309, 798)],
        28: [(105, 825), (136, 825), (164, 825), (194, 825), (222, 825), (252, 825), (280, 825) , (310, 825)],
        29: [(106, 851), (136, 852), (164, 852) , (195, 852), (223, 852), (252, 852), (280, 852) , (310, 852)],
        30: [(105, 878), (138, 878) , (165, 878), (195, 878), (224, 878), (252, 878), (280, 878) , (310, 878)],
        31: [(106, 908), (136, 908), (166, 908) , (195, 908), (224, 908), (254, 908), (282, 908) , (310, 908)],
        32: [(108, 935), (136, 935), (166, 935) , (195, 935), (224, 935), (254, 935), (282, 935) , (310, 935)],
        33: [(107, 961), (136, 961), (166, 961) , (195, 961), (226, 961), (255, 961), (282, 961) , (310, 961)],
        34: [(107, 989), (136, 989) , (168, 989), (195, 989), (226, 989), (255, 989), (282, 989) , (310, 989)],
        35: [(108, 1018), (138, 1018) , (168, 1018) , (195, 1018), (226, 1018), (255, 1018), (282, 1018) , (310, 1018)],
        36: [(108, 1044), (138, 1044), (168, 1044) , (195, 1044), (226, 1044), (255, 1044), (282, 1044) , (312, 1044)] ,

        37: [(406, 745),(440, 745),(466, 745) ,(494, 745) ,(523, 745) ,(557, 745) ,(585, 745) ,(613, 745)  ],
        38: [(407, 772) ,(440, 772),(466, 772) ,(494, 772) ,(523, 772) ,(557, 772) ,(585, 772) ,(613, 772)],
        39: [(407, 800) ,(440, 800),(466, 800) ,(494, 800) ,(523, 800) ,(557, 800) ,(585, 800) ,(613, 800)],
        40: [(408, 825) ,(440, 825),(466, 825) ,(494, 825) ,(523, 825) ,(557, 825) ,(585, 825) ,(613, 825)],
        41: [(410, 855) ,(440, 855),(470, 855) ,(498, 855) ,(527, 855) ,(557, 855) ,(585, 855) ,(613, 855)],
        42: [(410, 882) ,(440, 882),(470, 882) ,(498, 882) ,(527, 882) ,(557, 882) ,(585, 882) ,(613, 882)],
        43: [(410, 910) ,(440, 910),(470, 910) ,(498, 910) ,(527, 910) ,(557, 910) ,(585, 910) ,(613, 910)],
        44: [(410, 934) ,(440, 934),(469, 934) ,(498, 934) ,(527, 934) ,(557, 934) ,(585, 934) ,(613, 934)],
        45: [(410, 962) ,(440, 962),(469, 962) ,(498, 962) ,(527, 962) ,(557, 962) ,(585, 962) ,(613, 962)],
        46: [(410, 990) ,(440, 990),(469, 990) ,(498, 990) ,(527, 990) ,(557, 990) ,(585, 990) ,(613, 990)],
        47: [(412, 1020),(440, 1020),(469, 1020) ,(498, 1020) ,(527, 1020) ,(558, 1020) ,(585, 1020) ,(613, 1020) ],
        48: [(412, 1042),(440, 1043),(470, 1043) ,(498, 1045) ,(530, 1042) ,(558, 1042) ,(587, 1043) ,(615, 1043) ],

        49: [(712, 749), (741, 749), (770, 749) , (799, 749), (828, 749), (857, 749), (886, 749) , (915, 749)],
        50: [(713, 776), (741, 776), (770, 776) , (799, 776), (828, 776), (857, 776), (886, 776) , (915, 776)],
        51: [(713, 803), (741, 803), (770, 803) , (799, 803), (828, 803), (857, 803), (886, 803) , (915, 803)],
        52: [(713, 830), (741, 830), (770, 830) , (799, 830), (828, 830), (857, 830), (886, 830) , (915, 830)],
        53: [(714, 857), (743, 857), (772, 857) , (801, 857), (830, 857), (859, 857), (888, 857) , (917, 857)],
        54: [(714, 884), (743, 884), (772, 884) , (801, 884), (830, 884), (859, 884), (888, 884) , (917, 884)],
        55: [(714, 913), (743, 913), (772, 913) , (801, 913), (830, 913), (859, 913), (888, 913) , (917, 913)],
        56: [(715, 940), (744, 940), (773, 940) , (802, 940), (831, 940), (860, 940), (889, 940) , (918, 940)],
        57: [(715, 967), (744, 967), (773, 967) , (802, 967), (831, 967), (860, 967), (889, 967) , (918, 967)],
        58: [(715, 994), (744, 994), (773, 994) , (802, 994), (831, 994), (860, 994), (889, 994) , (918, 994)],
        59: [(716, 1022), (745, 1022), (774, 1022) , (803, 1022), (832, 1022), (861, 1022), (890, 1022) , (919, 1022)],
        60: [(716, 1049), (745, 1049), (774, 1049) , (803, 1049), (832, 1049), (861, 1049), (890, 1049) , (919, 1049)],
        
        
       
    }

    # Correct answer key
    answer_key = {1: 'D', 2: 'E', 3: 'A', 4: 'B', 5: 'F', 6: 'C', 7: 'F', 8: 'B', 9: 'A', 10: 'C', 11: 'D', 12: 'E',
        13: 'B', 14: 'F', 15: 'A', 16: 'B', 17: 'A', 18: 'C', 19: 'E', 20: 'F', 21: 'D', 22: 'C', 23: 'D', 24: 'E',
        25: 'H', 26: 'B', 27: 'C', 28: 'H', 29: 'G', 30: 'D', 31: 'E', 32: 'A', 33: 'G', 34: 'F', 35: 'A', 36: 'B',
        37: 'C', 38: 'D', 39: 'C', 40: 'G', 41: 'H', 42: 'F', 43: 'E', 44: 'D', 45: 'A', 46: 'B', 47: 'E', 48: 'F',
        49: 'G', 50: 'F', 51: 'H', 52: 'B', 53: 'A', 54: 'E', 55: 'A', 56: 'F', 57: 'C', 58: 'B', 59: 'D', 60: 'E'}
    
    marked_answers = {}
    
    # Visualize detection for debugging
    for question, bubbles in answer_bubbles.items():
        print(f"Processing Question {question} with bubbles {bubbles}")  # Debugging print
        marked_bubble_count = 0
        for i, (x, y) in enumerate(bubbles):
            # Draw rectangles on the image to visualize bubble positions
            cv2.circle(image, (x, y), 10, (255, 0, 0), 2)  # Blue circle with radius 20
            
            # Extract region of interest (ROI) for each bubble
            roi = thresh[y-20:y+20, x-20:x+20]  # Small region around the bubble
            
            # Check if the ROI is filled (marked)
            filled = cv2.countNonZero(roi)
            if filled > 500:  # Threshold for considering it marked
                marked_bubble_count += 1
                if marked_bubble_count > 1:  # Check for multiple marked bubbles
                    marked_answers[question] = None  # Award zero points if multiple marked
                    break  # No need to check further bubbles for this question
                else:
                    marked_answers[question] = chr(65 + i)  # 'A' is 65 in ASCII
                cv2.putText(image, "Marked", (x - 40, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Now draw the correct answer with a green box for visualization
        correct_answer = answer_key[question]
        correct_index = ord(correct_answer) - 65  # Convert 'A', 'B', 'C', 'D' to index 0, 1, 2, 3
        correct_x, correct_y = bubbles[correct_index]
        cv2.circle(image, (correct_x, correct_y), 10, (0, 0, 255), 2)  # red circle for correct answer
        # cv2.putText(image, "Correct", (correct_x - 40, correct_y - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Calculate the score
    correct_answers = 0
    for question, marked in marked_answers.items():
        if marked == answer_key[question]:
            correct_answers += 1
    
    # Save the debug image with marked areas and correct answers
    cv2.imwrite('marked_answer_sheet_updated.png', image)  # Save updated image with green boxes for correct answers
    
    
    return correct_answers

@app.route('/process_omr', methods=['POST'])
def process_omr():
    # Get the image URL from the incoming request
    image_url = request.json.get('image_url')
    
    # Get image data from URL (in memory, no saving to disk)
    img_data = requests.get(image_url).content
    image = np.asarray(bytearray(img_data), dtype=np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Process the image to calculate the score
    score = omr_processing(img)

    # Return the score as a JSON response
    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(debug=True)
