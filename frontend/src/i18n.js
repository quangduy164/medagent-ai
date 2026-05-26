const translations = {
  en: {
    // Header
    appTitle: 'X-Ray AI Agent',
    appSubtitle: 'Multi-Agent Chest X-Ray Analysis · DenseNet121 + ResNet50 Ensemble',

    // Upload
    uploadTitle: 'Upload X-Ray Image',
    uploadHint: 'Drag & drop or',
    uploadClick: 'click to select',
    uploadSub: 'PNG, JPG supported',
    notXray: 'Please upload a valid chest X-ray image. Color photos are not supported.',
    analyzeBtn: 'Analyze',
    analyzing: 'Analyzing...',

    // Analysis
    analysisTitle: 'Analysis Result',
    statusNormal: '✅ Normal',
    statusAbnormal: '⚠️ Abnormal',
    labelDiagnosis: 'Diagnosis',
    labelConfidence: 'Confidence',
    topProb: 'Top Probabilities',

    // Heatmap
    heatmapTitle: 'Grad-CAM Heatmap',
    heatmapOriginal: 'Original',
    heatmapActivation: 'Activation Map',

    // Report
    reportTitle: 'Radiology Report',

    // Disease names (kept in English as international standard)
    diseases: {
      'Atelectasis': 'Atelectasis',
      'Cardiomegaly': 'Cardiomegaly',
      'Consolidation': 'Consolidation',
      'Edema': 'Edema',
      'Effusion': 'Effusion',
      'Emphysema': 'Emphysema',
      'Fibrosis': 'Fibrosis',
      'Fracture': 'Fracture',
      'Hernia': 'Hernia',
      'Infiltration': 'Infiltration',
      'Lung Opacity': 'Lung Opacity',
      'Mass': 'Mass',
      'No Finding': 'No Finding',
      'Nodule': 'Nodule',
      'Pleural_Thickening': 'Pleural Thickening',
      'Pneumonia': 'Pneumonia',
      'Pneumothorax': 'Pneumothorax',
    },
  },

  vi: {
    // Header
    appTitle: 'AI Phân Tích X-Quang',
    appSubtitle: 'Hệ thống đa tác nhân · DenseNet121 + ResNet50 Ensemble',

    // Upload
    uploadTitle: 'Tải Ảnh X-Quang',
    uploadHint: 'Kéo thả hoặc',
    uploadClick: 'nhấn để chọn file',
    uploadSub: 'Hỗ trợ PNG, JPG',
    notXray: 'Vui lòng tải lên ảnh X-quang ngực hợp lệ. Ảnh màu thông thường không được hỗ trợ.',
    analyzeBtn: 'Phân Tích',
    analyzing: 'Đang phân tích...',

    // Analysis
    analysisTitle: 'Kết Quả Phân Tích',
    statusNormal: '✅ Bình Thường',
    statusAbnormal: '⚠️ Bất Thường',
    labelDiagnosis: 'Chẩn Đoán',
    labelConfidence: 'Độ Tin Cậy',
    topProb: 'Xác Suất Hàng Đầu',

    // Heatmap
    heatmapTitle: 'Bản Đồ Nhiệt Grad-CAM',
    heatmapOriginal: 'Ảnh Gốc',
    heatmapActivation: 'Bản Đồ Kích Hoạt',

    // Report
    reportTitle: 'Báo Cáo X-Quang',

    // Tên bệnh dịch chuyên ngành
    diseases: {
      'Atelectasis': 'Xẹp phổi',
      'Cardiomegaly': 'Tim to',
      'Consolidation': 'Đông đặc phổi',
      'Edema': 'Phù phổi',
      'Effusion': 'Tràn dịch màng phổi',
      'Emphysema': 'Khí phế thũng',
      'Fibrosis': 'Xơ phổi',
      'Fracture': 'Gãy xương sườn',
      'Hernia': 'Thoát vị hoành',
      'Infiltration': 'Thâm nhiễm phổi',
      'Lung Opacity': 'Mờ phổi',
      'Mass': 'Khối u phổi',
      'No Finding': 'Bình thường',
      'Nodule': 'Nốt phổi',
      'Pleural_Thickening': 'Dày màng phổi',
      'Pneumonia': 'Viêm phổi',
      'Pneumothorax': 'Tràn khí màng phổi',
    },
  },
};

export default translations;
