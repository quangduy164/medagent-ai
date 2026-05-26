# models/bridge.py
import random

# ── Templates tiếng Anh ──────────────────────────────────────────────────────
DISEASE_TEMPLATES_EN = {
    "No Finding": [
        "The lungs are clear. The heart size is normal. The mediastinal contours are unremarkable. No pleural effusion or pneumothorax is identified. The osseous structures are intact.",
        "No acute cardiopulmonary abnormality. The lungs are well expanded and clear. Heart size and mediastinal contours are within normal limits. No pleural effusion or pneumothorax.",
        "Clear lungs bilaterally. Normal cardiac silhouette. No focal consolidation, pleural effusion, or pneumothorax. Bony thorax is intact.",
    ],
    "Cardiomegaly": [
        "The cardiac silhouette is enlarged. The lungs are clear without focal consolidation. No pleural effusion or pneumothorax. The mediastinal contours are stable. Osseous structures are intact.",
        "Cardiomegaly is present. Pulmonary vascularity is within normal limits. No acute airspace disease. No pleural effusion identified. The bony thorax is unremarkable.",
        "Enlarged cardiac silhouette consistent with cardiomegaly. The lungs are clear. No evidence of pulmonary edema. No pneumothorax or pleural effusion.",
    ],
    "Effusion": [
        "There is a {size} pleural effusion on the {side}. The {side} costophrenic angle is blunted. The lungs are otherwise clear. No pneumothorax. Heart size is normal.",
        "Blunting of the {side} costophrenic angle consistent with {size} pleural effusion. No focal consolidation. Cardiac silhouette is within normal limits.",
        "{size} pleural effusion is noted on the {side}. There is associated compressive atelectasis. No pneumothorax identified.",
    ],
    "Pneumonia": [
        "There is a focal airspace opacity in the {location} consistent with pneumonia. No pleural effusion. Heart size is normal. The remaining lung fields are clear.",
        "Focal consolidation in the {location} suggestive of pneumonia or airspace disease. Clinical correlation is recommended. No pneumothorax or large effusion.",
        "Airspace disease in the {location}, most likely representing pneumonia. The cardiac silhouette is normal in size. No pleural effusion.",
    ],
    "Infiltration": [
        "Patchy airspace opacities are noted in the {location}, consistent with infiltration. No pleural effusion or pneumothorax. Heart size is normal.",
        "Ill-defined opacities in the {location} likely representing infiltrates. The cardiac silhouette is normal. No acute osseous abnormality.",
        "Bilateral patchy infiltrates are present, most prominent in the {location}. No pneumothorax. Heart size is stable.",
    ],
    "Atelectasis": [
        "Linear atelectasis is noted in the {location}. No focal consolidation or pleural effusion. Heart size is normal. No pneumothorax.",
        "Subsegmental atelectasis in the {location}. The lungs are otherwise clear. Cardiac silhouette is within normal limits.",
        "Plate-like atelectasis in the {location}. No pneumothorax or pleural effusion identified. Heart size is normal.",
    ],
    "Pneumothorax": [
        "There is a pneumothorax on the {side}. A visible pleural line is noted in the {location}. No tension physiology. The contralateral lung is clear.",
        "Small pneumothorax identified in the {location}. No mediastinal shift. Heart size is normal. No pleural effusion on the contralateral side.",
        "Pneumothorax is present in the {location}. The lung is partially collapsed. Clinical correlation and follow-up recommended.",
    ],
    "Nodule": [
        "A {size} pulmonary nodule is noted in the {location}. No other focal consolidation. Heart size is normal. Comparison with prior imaging is recommended.",
        "Nodular opacity in the {location}. No pleural effusion or pneumothorax. The cardiac silhouette is normal. Follow-up CT may be warranted.",
        "A {size} nodule is identified in the {location}. The remaining lung fields are clear. No acute cardiopulmonary abnormality.",
    ],
    "Mass": [
        "A {size} mass-like opacity is identified in the {location}. Further evaluation with CT is recommended. No pleural effusion. Heart size is normal.",
        "Large opacity in the {location} concerning for a mass lesion. No pneumothorax. Cardiac silhouette is within normal limits. CT correlation advised.",
        "A {size} mass is noted in the {location}. The mediastinum is not widened. No pleural effusion or pneumothorax identified.",
    ],
    "Edema": [
        "Diffuse bilateral interstitial opacities consistent with pulmonary edema. The cardiac silhouette is enlarged. Vascular congestion is present. No pneumothorax.",
        "Pulmonary vascular congestion and perihilar haziness consistent with pulmonary edema. Bilateral pleural effusions may be present. Cardiomegaly noted.",
        "Interstitial edema pattern bilaterally. Indistinct pulmonary vasculature. The heart is enlarged. No pneumothorax identified.",
    ],
    "Consolidation": [
        "Dense consolidation with air bronchograms in the {location}. No pleural effusion. Heart size is normal. The remaining lung fields are clear.",
        "Alveolar consolidation noted in the {location}. No pneumothorax or large effusion. Cardiac silhouette is within normal limits.",
        "Lobar consolidation in the {location} consistent with pneumonia or aspiration. No pleural effusion. Heart size is stable.",
    ],
    "Emphysema": [
        "Hyperinflated lungs with flattened diaphragms consistent with emphysema. Increased AP diameter. No focal consolidation or pleural effusion. Heart size is normal.",
        "Signs of chronic obstructive pulmonary disease with hyperlucency and flattened hemidiaphragms. No acute airspace disease. No pneumothorax.",
        "Emphysematous changes bilaterally. Barrel-shaped chest. No focal consolidation. Cardiac silhouette is within normal limits.",
    ],
    "Fibrosis": [
        "Reticular interstitial markings in the {location} suggestive of pulmonary fibrosis. No acute airspace disease. Heart size is normal.",
        "Chronic interstitial changes and fibrosis noted in the {location}. No pleural effusion or pneumothorax. Cardiac silhouette is stable.",
        "Bilateral reticular opacities consistent with fibrosis. Honeycombing may be present. No acute cardiopulmonary process identified.",
    ],
    "Pleural_Thickening": [
        "Pleural thickening is noted in the {location}. No acute airspace disease. Heart size is normal. No pneumothorax or effusion.",
        "Apical pleural thickening and scarring observed. The lungs are otherwise clear. Cardiac silhouette is within normal limits.",
        "Chronic pleural thickening in the {location}. No new focal consolidation. No pleural effusion. Heart size is stable.",
    ],
    "Hernia": [
        "A hiatal hernia is visible behind the cardiac silhouette. The lungs are clear. No pleural effusion or pneumothorax. Heart size is normal.",
        "Gas-filled structure projecting over the diaphragm consistent with hiatal hernia. No acute cardiopulmonary abnormality.",
        "Hiatal hernia noted. The lungs are clear bilaterally. Cardiac silhouette is within normal limits. No pleural effusion.",
    ],
    "Fracture": [
        "Rib fracture is noted in the {location}. No pneumothorax identified. The lungs are clear. Heart size is normal.",
        "Acute rib fracture in the {location}. No associated pneumothorax or hemothorax. Cardiac silhouette is within normal limits.",
        "Fracture of the {location} ribs. The lungs are otherwise clear. No pleural effusion or pneumothorax.",
    ],
    "Lung Opacity": [
        "Airspace opacity in the {location}. Differential includes pneumonia, atelectasis, or aspiration. No pleural effusion. Heart size is normal.",
        "Focal lung opacity noted in the {location}. Clinical correlation recommended. No pneumothorax. Cardiac silhouette is stable.",
        "Opacity in the {location} of uncertain etiology. No large pleural effusion. Heart size is within normal limits.",
    ],
}

IMPRESSION_TEMPLATES_EN = {
    "No Finding":         "No acute cardiopulmonary process.",
    "Cardiomegaly":       "Cardiomegaly. No acute pulmonary process.",
    "Effusion":           "{size} pleural effusion on the {side}.",
    "Pneumonia":          "Airspace disease in the {location}, pneumonia not excluded.",
    "Infiltration":       "Pulmonary infiltrates in the {location}.",
    "Atelectasis":        "Atelectasis in the {location}.",
    "Pneumothorax":       "Pneumothorax on the {side}. Clinical correlation advised.",
    "Nodule":             "Pulmonary nodule in the {location}. Follow-up recommended.",
    "Mass":               "Mass lesion in the {location}. CT recommended.",
    "Edema":              "Pulmonary edema with cardiomegaly.",
    "Consolidation":      "Consolidation in the {location}.",
    "Emphysema":          "Emphysema / COPD changes.",
    "Fibrosis":           "Pulmonary fibrosis in the {location}.",
    "Pleural_Thickening": "Pleural thickening in the {location}.",
    "Hernia":             "Hiatal hernia.",
    "Fracture":           "Rib fracture in the {location}.",
    "Lung Opacity":       "Lung opacity in the {location}. Clinical correlation recommended.",
}

# ── Templates tiếng Việt ─────────────────────────────────────────────────────
DISEASE_TEMPLATES_VI = {
    "No Finding": [
        "Hai phổi thông thoáng. Kích thước tim trong giới hạn bình thường. Trung thất không giãn rộng. Không có tràn dịch màng phổi hay tràn khí màng phổi. Cấu trúc xương ngực nguyên vẹn.",
        "Không có bất thường tim phổi cấp tính. Hai phổi nở tốt và thông thoáng. Kích thước tim và trung thất trong giới hạn bình thường. Không có tràn dịch hay tràn khí màng phổi.",
        "Hai phổi sáng đều. Bóng tim bình thường. Không có đông đặc khu trú, tràn dịch màng phổi hay tràn khí màng phổi. Lồng ngực xương bình thường.",
    ],
    "Cardiomegaly": [
        "Bóng tim to. Hai phổi thông thoáng, không có đông đặc khu trú. Không có tràn dịch hay tràn khí màng phổi. Trung thất ổn định. Cấu trúc xương nguyên vẹn.",
        "Tim to. Tuần hoàn phổi trong giới hạn bình thường. Không có bệnh lý khoang khí cấp tính. Không có tràn dịch màng phổi. Lồng ngực xương không có bất thường.",
        "Bóng tim to phù hợp với tim to. Hai phổi thông thoáng. Không có bằng chứng phù phổi. Không có tràn khí hay tràn dịch màng phổi.",
    ],
    "Effusion": [
        "Có tràn dịch màng phổi {size} bên {side}. Góc sườn hoành bên {side} bị tù. Phổi còn lại thông thoáng. Không có tràn khí màng phổi. Kích thước tim bình thường.",
        "Góc sườn hoành bên {side} bị tù phù hợp với tràn dịch màng phổi {size}. Không có đông đặc khu trú. Bóng tim trong giới hạn bình thường.",
        "Tràn dịch màng phổi {size} bên {side}. Có xẹp phổi do chèn ép kèm theo. Không có tràn khí màng phổi.",
    ],
    "Pneumonia": [
        "Có mờ khoang khí khu trú tại {location} phù hợp với viêm phổi. Không có tràn dịch màng phổi. Kích thước tim bình thường. Các vùng phổi còn lại thông thoáng.",
        "Đông đặc khu trú tại {location} gợi ý viêm phổi hoặc bệnh lý khoang khí. Cần đối chiếu lâm sàng. Không có tràn khí hay tràn dịch màng phổi lớn.",
        "Bệnh lý khoang khí tại {location}, nhiều khả năng là viêm phổi. Bóng tim kích thước bình thường. Không có tràn dịch màng phổi.",
    ],
    "Infiltration": [
        "Ghi nhận mờ khoang khí dạng đốm tại {location}, phù hợp với thâm nhiễm. Không có tràn dịch hay tràn khí màng phổi. Kích thước tim bình thường.",
        "Mờ không rõ bờ tại {location} có thể là thâm nhiễm. Bóng tim bình thường. Không có bất thường xương cấp tính.",
        "Thâm nhiễm dạng đốm hai bên, rõ nhất tại {location}. Không có tràn khí màng phổi. Kích thước tim ổn định.",
    ],
    "Atelectasis": [
        "Xẹp phổi dạng dải tại {location}. Không có đông đặc khu trú hay tràn dịch màng phổi. Kích thước tim bình thường. Không có tràn khí màng phổi.",
        "Xẹp phổi phân thùy tại {location}. Phổi còn lại thông thoáng. Bóng tim trong giới hạn bình thường.",
        "Xẹp phổi dạng tấm tại {location}. Không có tràn khí hay tràn dịch màng phổi. Kích thước tim bình thường.",
    ],
    "Pneumothorax": [
        "Có tràn khí màng phổi bên {side}. Ghi nhận đường màng phổi tại {location}. Không có sinh lý căng. Phổi đối bên thông thoáng.",
        "Tràn khí màng phổi nhỏ tại {location}. Không có lệch trung thất. Kích thước tim bình thường. Không có tràn dịch màng phổi bên đối diện.",
        "Tràn khí màng phổi tại {location}. Phổi xẹp một phần. Cần đối chiếu lâm sàng và theo dõi.",
    ],
    "Nodule": [
        "Ghi nhận nốt phổi {size} tại {location}. Không có đông đặc khu trú khác. Kích thước tim bình thường. Cần so sánh với phim cũ.",
        "Mờ dạng nốt tại {location}. Không có tràn dịch hay tràn khí màng phổi. Bóng tim bình thường. Có thể cần chụp CT theo dõi.",
        "Nốt {size} tại {location}. Các vùng phổi còn lại thông thoáng. Không có bất thường tim phổi cấp tính.",
    ],
    "Mass": [
        "Ghi nhận mờ dạng khối {size} tại {location}. Cần đánh giá thêm bằng CT. Không có tràn dịch màng phổi. Kích thước tim bình thường.",
        "Mờ lớn tại {location} gợi ý tổn thương dạng khối. Không có tràn khí màng phổi. Bóng tim trong giới hạn bình thường. Cần đối chiếu CT.",
        "Khối {size} tại {location}. Trung thất không giãn rộng. Không có tràn dịch hay tràn khí màng phổi.",
    ],
    "Edema": [
        "Mờ mô kẽ lan tỏa hai bên phù hợp với phù phổi. Bóng tim to. Có ứ huyết mạch máu. Không có tràn khí màng phổi.",
        "Ứ huyết mạch máu phổi và mờ quanh rốn phổi phù hợp với phù phổi. Có thể có tràn dịch màng phổi hai bên. Ghi nhận tim to.",
        "Hình ảnh phù mô kẽ hai bên. Mạch máu phổi không rõ nét. Tim to. Không có tràn khí màng phổi.",
    ],
    "Consolidation": [
        "Đông đặc đậm với hình ảnh phế quản hơi tại {location}. Không có tràn dịch màng phổi. Kích thước tim bình thường. Các vùng phổi còn lại thông thoáng.",
        "Đông đặc phế nang tại {location}. Không có tràn khí hay tràn dịch màng phổi lớn. Bóng tim trong giới hạn bình thường.",
        "Đông đặc thùy tại {location} phù hợp với viêm phổi hoặc hít sặc. Không có tràn dịch màng phổi. Kích thước tim ổn định.",
    ],
    "Emphysema": [
        "Hai phổi ứ khí với cơ hoành dẹt phù hợp với khí phế thũng. Đường kính trước sau tăng. Không có đông đặc khu trú hay tràn dịch màng phổi. Kích thước tim bình thường.",
        "Dấu hiệu bệnh phổi tắc nghẽn mạn tính với tăng sáng phổi và cơ hoành dẹt. Không có bệnh lý khoang khí cấp tính. Không có tràn khí màng phổi.",
        "Thay đổi khí phế thũng hai bên. Lồng ngực hình thùng. Không có đông đặc khu trú. Bóng tim trong giới hạn bình thường.",
    ],
    "Fibrosis": [
        "Hình ảnh lưới mô kẽ tại {location} gợi ý xơ phổi. Không có bệnh lý khoang khí cấp tính. Kích thước tim bình thường.",
        "Thay đổi mô kẽ mạn tính và xơ hóa tại {location}. Không có tràn dịch hay tràn khí màng phổi. Bóng tim ổn định.",
        "Mờ lưới hai bên phù hợp với xơ phổi. Có thể có hình ảnh tổ ong. Không có bệnh lý tim phổi cấp tính.",
    ],
    "Pleural_Thickening": [
        "Dày màng phổi tại {location}. Không có bệnh lý khoang khí cấp tính. Kích thước tim bình thường. Không có tràn khí hay tràn dịch màng phổi.",
        "Dày và xơ màng phổi đỉnh phổi. Phổi còn lại thông thoáng. Bóng tim trong giới hạn bình thường.",
        "Dày màng phổi mạn tính tại {location}. Không có đông đặc mới. Không có tràn dịch màng phổi. Kích thước tim ổn định.",
    ],
    "Hernia": [
        "Thoát vị hoành thực quản thấy sau bóng tim. Hai phổi thông thoáng. Không có tràn dịch hay tràn khí màng phổi. Kích thước tim bình thường.",
        "Cấu trúc chứa khí nhô lên trên cơ hoành phù hợp với thoát vị hoành. Không có bất thường tim phổi cấp tính.",
        "Thoát vị hoành. Hai phổi thông thoáng. Bóng tim trong giới hạn bình thường. Không có tràn dịch màng phổi.",
    ],
    "Fracture": [
        "Gãy xương sườn tại {location}. Không có tràn khí màng phổi. Hai phổi thông thoáng. Kích thước tim bình thường.",
        "Gãy xương sườn cấp tính tại {location}. Không có tràn khí hay tràn máu màng phổi kèm theo. Bóng tim trong giới hạn bình thường.",
        "Gãy xương sườn {location}. Phổi còn lại thông thoáng. Không có tràn dịch hay tràn khí màng phổi.",
    ],
    "Lung Opacity": [
        "Mờ khoang khí tại {location}. Chẩn đoán phân biệt gồm viêm phổi, xẹp phổi hoặc hít sặc. Không có tràn dịch màng phổi. Kích thước tim bình thường.",
        "Mờ phổi khu trú tại {location}. Cần đối chiếu lâm sàng. Không có tràn khí màng phổi. Bóng tim ổn định.",
        "Mờ tại {location} chưa rõ nguyên nhân. Không có tràn dịch màng phổi lớn. Kích thước tim trong giới hạn bình thường.",
    ],
}

IMPRESSION_TEMPLATES_VI = {
    "No Finding":         "Không có bệnh lý tim phổi cấp tính.",
    "Cardiomegaly":       "Tim to. Không có bệnh lý phổi cấp tính.",
    "Effusion":           "Tràn dịch màng phổi {size} bên {side}.",
    "Pneumonia":          "Bệnh lý khoang khí tại {location}, không loại trừ viêm phổi.",
    "Infiltration":       "Thâm nhiễm phổi tại {location}.",
    "Atelectasis":        "Xẹp phổi tại {location}.",
    "Pneumothorax":       "Tràn khí màng phổi bên {side}. Cần đối chiếu lâm sàng.",
    "Nodule":             "Nốt phổi tại {location}. Cần theo dõi.",
    "Mass":               "Tổn thương dạng khối tại {location}. Cần chụp CT.",
    "Edema":              "Phù phổi kèm tim to.",
    "Consolidation":      "Đông đặc phổi tại {location}.",
    "Emphysema":          "Khí phế thũng / COPD.",
    "Fibrosis":           "Xơ phổi tại {location}.",
    "Pleural_Thickening": "Dày màng phổi tại {location}.",
    "Hernia":             "Thoát vị hoành.",
    "Fracture":           "Gãy xương sườn tại {location}.",
    "Lung Opacity":       "Mờ phổi tại {location}. Cần đối chiếu lâm sàng.",
}

# ── Alias để backward-compat ─────────────────────────────────────────────────
DISEASE_TEMPLATES   = DISEASE_TEMPLATES_EN
IMPRESSION_TEMPLATES = IMPRESSION_TEMPLATES_EN


def _fill(template: str, location: str, size: str, side: str) -> str:
    return (template
            .replace("{location}", location)
            .replace("{size}", size)
            .replace("{side}", side))


def generate_prompt(
    diagnosis: str,
    confidence: float,
    location: str = "chest",
    size: str = "moderate",
    side: str = "unspecified",
    threshold: float = 0.45,
    lang: str = "en",
) -> str:
    """
    Sinh report Findings + Impression theo ngôn ngữ chỉ định (en/vi).
    """
    templates   = DISEASE_TEMPLATES_VI   if lang == "vi" else DISEASE_TEMPLATES_EN
    impressions = IMPRESSION_TEMPLATES_VI if lang == "vi" else IMPRESSION_TEMPLATES_EN

    key = diagnosis if diagnosis in templates else "No Finding"

    # Dùng hash của diagnosis làm seed để luôn chọn cùng template cho cùng 1 ảnh
    rng = random.Random(hash(diagnosis))
    findings   = _fill(rng.choice(templates[key]), location, size, side)
    impression = _fill(impressions.get(key, impressions["No Finding"]), location, size, side)

    label_f = "Kết quả:" if lang == "vi" else "Findings:"
    label_i = "Kết luận:" if lang == "vi" else "Impression:"

    return f"{label_f} {findings} {label_i} {impression}"
