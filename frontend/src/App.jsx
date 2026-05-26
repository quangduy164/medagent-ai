import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import translations from './i18n';
import flagEN from './assets/english.png';
import flagVI from './assets/vietnam.png';
import logo   from './assets/logo.png';
import UploadCard   from './components/UploadCard';
import AnalysisCard from './components/AnalysisCard';
import ReportPanel  from './components/ReportPanel';
import SamplePickerModal from './components/SamplePickerModal';

const API      = '/analyze-image';
const IMG_BASE = 'http://localhost:8000';

export default function App() {
  const [file, setFile]         = useState(null);
  const [preview, setPreview]   = useState(null);
  const [result, setResult]     = useState(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);
  const [errorKey, setErrorKey] = useState(null); // key vào i18n, tự đổi theo lang
  const [lang, setLang]         = useState('vi'); // mặc định tiếng Việt
  const [report, setReport]     = useState(null);
  const [showSamples, setShowSamples] = useState(false);
  const inputRef                = useRef();
  const t = translations[lang];

  // error message: nếu có errorKey thì lấy từ i18n (tự đổi khi đổi lang)
  const errorMsg = errorKey ? t[errorKey] : error;

  useEffect(() => {
    if (result) setReport(result.report);
  }, [result]);

  useEffect(() => {
    if (!result) return;
    const findings = result.visual_findings || {};
    const form = new FormData();
    form.append('diagnosis',  result.diagnosis);
    form.append('confidence', result.confidence);
    form.append('location',   findings.location || 'chest');
    form.append('size',       findings.size     || 'moderate');
    form.append('side',       findings.side     || 'unspecified');
    form.append('lang',       lang);
    fetch('/translate-report', { method: 'POST', body: form })
      .then(r => r.json())
      .then(j => { if (j.success) setReport(j.report); })
      .catch(() => {});
  }, [lang]); // eslint-disable-line

  const checkIsXray = (f) => new Promise((resolve) => {
    const url = URL.createObjectURL(f);
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const size = 200;
      canvas.width = size;
      canvas.height = size;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, size, size);
      const { data } = ctx.getImageData(0, 0, size, size);
      let saturatedPixels = 0;
      const total = size * size;
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i] / 255, g = data[i + 1] / 255, b = data[i + 2] / 255;
        const max = Math.max(r, g, b), min = Math.min(r, g, b);
        const lightness = (max + min) / 2;
        // Tính saturation theo HSL
        const sat = (max === min) ? 0
          : lightness < 0.5
            ? (max - min) / (max + min)
            : (max - min) / (2 - max - min);
        // Pixel có màu rõ: saturation > 15% và không quá tối/sáng
        if (sat > 0.15 && lightness > 0.1 && lightness < 0.95) saturatedPixels++;
      }
      URL.revokeObjectURL(url);
      // X-quang thật: < 8% pixel có màu; ảnh thường: thường > 8%
      resolve(saturatedPixels / total < 0.08);
    };
    img.onerror = () => { URL.revokeObjectURL(url); resolve(false); };
    img.src = url;
  });

  // Chọn ảnh mẫu từ URL — bỏ qua checkIsXray vì đây là ảnh X-quang đã được kiểm duyệt
  const handleSampleSelect = async (url, filename) => {
    setShowSamples(false);
    setResult(null);
    setReport(null);
    setError(null);
    setErrorKey(null);
    try {
      // url là đường dẫn tương đối, proxy sẽ forward về backend
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const f = new File([blob], filename, { type: blob.type || 'image/png' });
      setFile(f);
      setPreview(URL.createObjectURL(blob));
    } catch (e) {
      setError(`Không thể tải ảnh mẫu: ${e.message}`);
    }
  };

  const handleFile = async (f) => {
    if (!f) return;
    setResult(null);
    setReport(null);
    setError(null);
    setErrorKey(null);
    const isXray = await checkIsXray(f);
    if (!isXray) {
      setFile(null);
      setPreview(null);
      setErrorKey('notXray'); // lưu key, không lưu string cứng
      return;
    }
    setFile(f);
    setPreview(URL.createObjectURL(f));
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setErrorKey(null);
    setResult(null);
    try {
      const form = new FormData();
      form.append('file', file);
      const res  = await fetch(`${API}?lang=${lang}`, { method: 'POST', body: form });
      const json = await res.json();
      if (!json.success) {
        if (json.error_code === 'not_xray') {
          setErrorKey('notXray');
        } else {
          throw new Error(json.error || 'Server error');
        }
        return;
      }
      setResult(json.data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const heatmapUrl = result?.heatmap_path
    ? `${IMG_BASE}/outputs/${result.heatmap_path.replace(/\\/g, '/').split('/').pop()}`
    : null;

  const isAbnormal = result && result.status !== 'Normal';

  const uploadProps = {
    t, preview, file, loading,
    error: errorMsg,
    inputRef,
    onFileChange:   (e) => handleFile(e.target.files[0]),
    onDrop:         (e) => { e.preventDefault(); handleFile(e.dataTransfer.files[0]); },
    onAnalyze:      handleAnalyze,
    onOpenSamples:  () => setShowSamples(true),
  };

  return (
    <div className="app">
      {showSamples && (
        <SamplePickerModal
          t={t}
          onSelect={handleSampleSelect}
          onClose={() => setShowSamples(false)}
        />
      )}
      <header className="header">
        <div className="header-brand">
          <img src={logo} alt="MedAgent AI" className="header-logo" />
          <div className="header-text">
            <h1>MedAgent AI</h1>
            <p>{t.appSubtitle}</p>
          </div>
        </div>
        <button
          className={`lang-toggle ${lang === 'vi' ? 'lang-vi' : 'lang-en'}`}
          onClick={() => setLang(l => l === 'en' ? 'vi' : 'en')}
          aria-label="Switch language"
        >
          <span className="lang-knob">
            <img src={lang === 'en' ? flagEN : flagVI} alt={lang} className="lang-flag" />
          </span>
          <span className="lang-label">{lang === 'en' ? 'EN' : 'VI'}</span>
        </button>
      </header>

      <div className="content">
        {!result && (
          <div className="layout-single">
            <UploadCard {...uploadProps} />
          </div>
        )}

        {result && !isAbnormal && (
          <div className="layout-two layout-two--equal">
            <UploadCard {...uploadProps} />
            <AnalysisCard result={result} preview={null} heatmapUrl={null} t={t} />
          </div>
        )}

        {result && isAbnormal && (
          <div className="layout-two">
            <div className="left-col">
              <UploadCard {...uploadProps} />
              <ReportPanel report={report || result.report} t={t} />
            </div>
            <AnalysisCard result={result} preview={preview} heatmapUrl={heatmapUrl} stretch t={t} />
          </div>
        )}

        {result && !isAbnormal && (
          <div style={{ marginTop: 24 }}>
            <ReportPanel report={report || result.report} t={t} />
          </div>
        )}
      </div>
    </div>
  );
}
