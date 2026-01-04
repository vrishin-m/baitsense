import color
import face
import nlp
import ocr
import overediting

def clickbait_or_not(file_path, title):
    print(title)
    emo_score, size =face.emo_score(file_path)
    text_score = nlp.clickbait_score(title)
    color_score = color.color_score(file_path)
    ocr_score = ocr.ocr_score(file_path)
    edit_score = overediting.edit_score(file_path)
    print(f"emo: {emo_score}, size: {size}, title: {text_score}, color: {color_score}, ocr: {ocr_score}, edit: {edit_score}")
    print(title)
    final_score = (emo_score*3 + text_score*6 + color_score + ocr_score *3 + edit_score*4 + size*0.5)/17.5
    print(final_score)
    if final_score >=0.6:
        print("clickbait")
        return "clickbait"
    else:
        print("not clickbait")
        return "not clickbait"
